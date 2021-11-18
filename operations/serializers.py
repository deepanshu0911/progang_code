from rest_framework import serializers
from operations.models import ProgangUser, Consultation, Quotation, Proposal

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProgangUser
        fields = ('id','google_id', 'photoUrl', 'firstName',
        'lastName', 'email', 'mobile', 'country', 'state', 'city', 'organisation','profileImg')

class ConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ('consult_id', 'user_id', 'name', 'email', 'mobile', 
        'consultType', 'slot', 'date')

class QuotationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Quotation
        fields = ('quote_id','user_id', 'name', 'emailOrMobile',
        'platform', 'requirements', 'date', 'quoteFile')        

class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ('proposal_id', 'user_id', 'name', 'email',
        'mobile', 'platform', 'requirements', 'date', 'pdfFile',
        'proposalFile')
