from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view ,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Cagnotte, Don, JustificationDon ,Donateur 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime


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

@api_view(['POST'])
def justifier_don(request):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    cagnotte_id = request.data.get('cagnotte_id')
    montant_justifie = request.data.get('montant_justifie')
    description = request.data.get('description')

    try:
        cagnotte = Cagnotte.objects.get(id=cagnotte_id)
    except Cagnotte.DoesNotExist:
        return Response({'error': 'Cagnotte non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    if montant_justifie > cagnotte.montant_actuel:
        return Response({'error': 'Le montant justifié dépasse le montant actuel de la cagnotte'}, status=status.HTTP_400_BAD_REQUEST)

    justification = JustificationDon.objects.create(cagnotte=cagnotte, montant_justifie=montant_justifie, description=description)
    cagnotte.montant_actuel -= montant_justifie
    cagnotte.save()

    return Response({'message': 'Justification effectuée avec succès'}, status=status.HTTP_201_CREATED)
