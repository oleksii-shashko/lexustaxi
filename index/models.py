from django.db import models
from . import validators


class Car(models.Model):
    """
    Model representing a type of car(e.g. Econom)
    """
    name = models.CharField(max_length=20, help_text="Enter car name of type")
    coast_per_km = models.IntegerField(validators=[validators.validate_more_then_zero], help_text="Enter coast per km")
    img_url = models.TextField(blank=True, null=True, help_text="Enter image path")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        :return: type name
        """
        return self.name


class Address(models.Model):
    """
    Model representing an address
    """
    city = models.CharField(max_length=50, help_text="Enter city")
    street = models.CharField(max_length=50, help_text="Enter street")
    house = models.IntegerField(help_text="Enter number of house")

    def __str__(self):
        """
        String for representing the Model object
        :return: address
        """
        return "г.{0}, ул.(пр.,пер.){1}, д.{2}".format(self.city, self.street, self.house)


class Distance(models.Model):
    """
    Model representing a distance between two addresses
    """
    distance = models.FloatField(validators=[validators.validate_more_then_zero], help_text="Enter distance in km")
    from_address = models.ForeignKey('Address', on_delete=models.CASCADE, null=False, related_name="from+")
    to_address = models.ForeignKey('Address', on_delete=models.CASCADE, null=False, related_name="to")

    def __str__(self):
        """
        String for representing the Model object
        :return: distance between two addresses
        """
        return "{0} km между {1} и {2}".format(self.distance, self.from_address, self.to_address)


class Client(models.Model):
    """
    Model representing a site client
    """
    login = models.CharField(max_length=20, help_text="Enter users login", null=False)
    password = models.CharField(max_length=20, help_text="Enter clients password", null=False)
    name = models.CharField(max_length=20, help_text="Enter clients name")
    phone_number = models.CharField(max_length=19, help_text="Enter phone number of client", null=False)

    LOAN_ROLL = (
        ('c', 'Client'),
        ('a', 'Admin'),
    )

    roll = models.CharField(max_length=1, choices=LOAN_ROLL, blank=False, default='c',
                            help_text="Enter users site roll")

    class Meta:
        ordering = ["phone_number"]

    def __str__(self):
        """
        String for representing the Model object
        :return: client
        """
        if self.roll is 'c':
            roll_index = 0
        else:
            roll_index = 1
        return "{0} {1}(login: {2}; phone number: {3})".format(self.LOAN_ROLL[roll_index][1], self.name, self.login, self.phone_number)


class Request(models.Model):
    """
    Model representing clients request for taxi
    """
    LOAN_STATUS = (
        ('a', 'Accepted'),
        ('r', 'Rejected'),
        ('u', 'Undefined'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=False, default='u',
                              help_text="Enter request status")
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=False)
    car = models.ForeignKey('Car', on_delete=models.CASCADE, null=False)
    distance = models.ForeignKey('Distance', on_delete=models.CASCADE, null=False)
    comment = models.TextField(max_length=256, null=True, blank=True,  help_text="Enter comments to request")
    data = models.DateField(null=False, blank=False)
    total = models.PositiveIntegerField(editable=False, default=0)

    class Meta:
        ordering = ("-data", "-status", "-id",)

    def __str__(self):
        """
        String for representing the Model object
        :return: request
        """
        return "{0} requested car {1}. It will be coast {2}".format(self.client, self.car, self.total)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        self.total = self.car.coast_per_km * self.distance.distance
        super(Request, self).save(*args, **kwargs)
