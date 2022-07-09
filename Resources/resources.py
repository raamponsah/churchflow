from import_export import resources
from import_export.fields import Field
from import_export.resources import Resource

# class BookResource(resources.ModelResource):
#
#     class Meta:
#         model = Book
#         fields = ('id', 'name', 'author', 'price',)
#         export_order = ('id', 'price', 'author', 'name')
from offerings.models import Offering
from pledges.models import MonetaryPledge


class OfferingResource(resources.ModelResource):
    service__title = Field(attribute='service__title', column_name='Service')
    type_of_offering__type_of_offering = Field(attribute='type_of_offering__type_of_offering', column_name='Offering '
                                                                                                           'Type')

    class Meta:
        model = Offering
        fields = ('service__title', 'type_of_offering__type_of_offering', 'created_on', 'amount')


class PledgeResource(resources.ModelResource):
    class Meta:
        model = MonetaryPledge
        fields = ('pledge_person', 'phone_number', 'amount_paid', 'amount_pledged', 'created_on')