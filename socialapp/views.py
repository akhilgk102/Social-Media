from django.shortcuts import render,get_object_or_404

# Create your views here.

from rest_framework.generics import CreateAPIView
from socialapp.serializers import UserCreationSerializer,PostSerializer,CommentSerializer,UserProfileSerializer

from rest_framework.generics import ListAPIView,CreateAPIView,DestroyAPIView,UpdateAPIView,RetrieveAPIView

from rest_framework.views import APIView

from socialapp.models import Post,Profile

from rest_framework import authentication,permissions

from rest_framework.response import Response


class SignUpView(CreateAPIView):

    serializer_class=UserCreationSerializer


class PostListCreateView(ListAPIView,CreateAPIView):

    serializer_class=PostSerializer

    queryset=Post.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)


    def get_serializer_context(self):
        context= super().get_serializer_context()

        context["request"]=self.request

        return context


class PostRetrieveUpdateDestroyView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):

    serializer_class=PostSerializer

    queryset=Post.objects.all()

    permission_classes=[permissions.IsAuthenticated]

    authentication_classes=[authentication.TokenAuthentication]


class PostLikeView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        post_object=get_object_or_404(Post,id=id)

        liked=False

        if request.user in post_object.liked_by.all():

            post_object.liked_by.remove(request.user)

        else:

            post_object.liked_by.add(request.user)
            liked=True


        return Response(data={"message":"liked","liked":liked})
    

class PostCommentView(CreateAPIView):

    serializer_class=CommentSerializer

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        post_object=get_object_or_404(Post,id=id)

        serializer_instance=self.serializer_class(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user,post=post_object)

            return Response(data=serializer_instance.data)
        
        return Response(data=serializer_instance.errors)


class ProfileUpdateView(UpdateAPIView):

    serializer_class=UserProfileSerializer

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def get_object(self):
        
        return Profile.objects.get(owner=self.request.user)
    