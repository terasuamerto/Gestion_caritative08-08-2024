from .models  import *
from rest_framework import status
from rest_framework.decorators import api_view ,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime
from django.contrib.auth import get_user_model



@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Tous les champs sont obligatoires'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Un utilisateur avec cet email existe déjà'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create(
            username=username,
            email=email,
            password=password
        )

        return Response({'message': 'Inscription réussie'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'L\'email et le mot de passe sont obligatoires'}, status=status.HTTP_400_BAD_REQUEST)

    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
         return Response({'error': 'Email ou mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)


    user = authenticate(request, username=user.username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'Connexion réussie', 'token': token.key}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Email ou mot de passe incorrectes'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def creer_cagnotte(request):
    intitule = request.data.get('intitule')
    description = request.data.get('description')
    objectif_montant_vise = request.data.get('objectif_montant_vise')
    image = request.FILES.get('image')  

    if not intitule or not description or not objectif_montant_vise:
        return Response({'error': 'Tous les champs obligatoires doivent être renseignés'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cagnotte = Cagnotte.objects.create(
            intitule=intitule,
            description=description,
            objectif_montant_vise=objectif_montant_vise,
            date_debut=datetime.now(),
            image=image,
            montant_collecte=0,
            created_by=request.user
        )
        return Response({'message': 'Cagnotte créée avec succès'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def details_cagnotte(request, cagnotte_id):
    try:
        cagnotte = Cagnotte.objects.get(id=cagnotte_id)
    except Cagnotte.DoesNotExist:
        return Response({'error': 'Cagnotte non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    cagnotte_details = {
        'intitule': cagnotte.intitule,
        'description': cagnotte.description,
        'objectif_montant_vise': cagnotte.objectif_montant_vise,
        'montant_collecte': cagnotte.montant_collecte,
        'date_debut': cagnotte.date_debut,
        'image': cagnotte.image.url 
    }

    dons = Don.objects.filter(cagnotte=cagnotte)
    dons_list = [
        {
            'montant': don.montant,
            'nom_donateur': don.donateur.nom if don.donateur else None,
            'prenom_donateur': don.donateur.prenom if don.donateur else None,
            'email_donateur': don.donateur.email if don.donateur else None,
            'date_don': don.date_don,
        }
        for don in dons
    ]

    return Response({
        'cagnotte': cagnotte_details,
        'dons': dons_list,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def liste_cagnottes(request):
    cagnottes = Cagnotte.objects.all()
    data = [
        {
            'intitule': cagnotte.intitule,
            'description': cagnotte.description,
            'montant_collecte': cagnotte.montant_collecte,
            'objectif_montant_vise': cagnotte.objectif_montant_vise,
            'date_debut': cagnotte.date_debut,
            'image_url': cagnotte.image.url,
            'created_by': cagnotte.created_by.username
        }
        for cagnotte in cagnottes
    ]
    return Response(data, status=status.HTTP_200_OK)
  
@api_view(['POST'])
def faire_don(request):
    cagnotte_id = request.data.get('cagnotte_id')
    montant = request.data.get('montant')
    nom = request.data.get('nom')
    prenom = request.data.get('prenom')
    email = request.data.get('email')

    if not cagnotte_id or not montant or not nom or not prenom or not email:
        return Response({'error': 'Tous les champs sont requis'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cagnotte = Cagnotte.objects.get(id=cagnotte_id)
    except Cagnotte.DoesNotExist:
        return Response({'error': 'Cagnotte non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    
    donateur, created = Donateur.objects.get_or_create(
        nom=nom,
        prenom=prenom,
        email=email
    )


    don = Don.objects.create(
        montant=montant,
        cagnotte=cagnotte,
        donateur=donateur,
        date_don=datetime.now()
    )

    cagnotte.montant_collecte += montant
    cagnotte.save()

    return Response({'message': 'Don effectué avec succès'}, status=status.HTTP_201_CREATED)
