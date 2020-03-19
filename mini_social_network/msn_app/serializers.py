from rest_framework import serializers

from msn_app.models import Post, Like, UserProfile, User
from msn_app.query import NUMBER_OF_LIKES_QUERY, IS_LIKED_QUERY


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'country', 'city')


class UserSerializerGetData(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                view_name='post-detail')
    likes = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                view_name='like-detail')

    class Meta:
        model = User
        fields = ('url', 'id', 'date_joined', 'password', 'first_name',
                  'last_name', 'email', 'profile', 'posts', 'likes')
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializerManipulateData(serializers.HyperlinkedModelSerializer):
    date_of_birth = serializers.DateField(required=True, write_only=True)
    country = serializers.CharField(max_length=255, required=True,
                                    write_only=True)
    city = serializers.CharField(max_length=255, required=True,
                                 write_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'date_joined', 'password', 'first_name',
                  'last_name', 'email', 'date_of_birth', 'country', 'city')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        date_of_birth = validated_data.pop('date_of_birth')
        country = validated_data.pop('country')
        city = validated_data.pop('city')

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, date_of_birth=date_of_birth,
                                   country=country, city=city)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        instance.save()

        profile = UserProfile.objects.get(user=instance)
        profile.date_of_birth = validated_data.get('date_of_birth',
                                                   profile.date_of_birth)
        profile.country = validated_data.get('country', profile.country)
        profile.city = validated_data.get('city', profile.city)
        profile.save()
        return instance


class PostSerializer(serializers.HyperlinkedModelSerializer):
    likes = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                view_name='like-detail')
    number_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('url', 'id', 'created', 'owner', 'text', 'likes',
                  'number_of_likes')
        read_only_fields = ('created', 'owner')

    def get_number_of_likes(self, obj):
        likes = Like.objects.raw(NUMBER_OF_LIKES_QUERY, [obj.id])
        number_of_likes = sum([int(x.is_liked) for x in likes])
        return number_of_likes


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(),
                                                 write_only=True)

    class Meta:
        model = Like
        fields = ('url', 'id', 'post', 'post_id', 'owner', 'created', 'is_liked')
        read_only_fields = ('created', 'post', 'owner', 'is_liked')

    def create(self, validated_data):
        post_id = validated_data.pop('post_id').id
        owner_id = validated_data['owner'].id
        params = [owner_id, post_id, owner_id, post_id]
        is_liked_now = Like.objects.raw(IS_LIKED_QUERY, params)
        if len(is_liked_now) == 0:
            like_action = True
        else:
            like_action = not is_liked_now[0].is_liked
        like = Like(is_liked=like_action, post_id=post_id, **validated_data)
        like.save()
        return like
