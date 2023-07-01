from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    population = models.IntegerField(default=0, null=True)
    area = models.FloatField(default=0, null=True)
    shape = models.FileField(upload_to='shapes/', null=True)
    flag = models.ImageField(upload_to='flags/', null=True)

    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    population = models.IntegerField(default=0, null=True)
    latitude = models.FloatField(default=0, null=True)
    longitude = models.FloatField(default=0, null=True)

    def __str__(self):
        return self.name
    
class League(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    level = models.IntegerField(default=0, null=True)
    logo = models.ImageField(upload_to='league_logos/', null=True)

    def __str__(self):
        return self.name
    
class Season(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.league.name + " " + str(self.start_date.year) + "-" + str(self.end_date.year)
    
class Stadium(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0, null=True)
    latitude = models.FloatField(default=0, null=True)
    longitude = models.FloatField(default=0, null=True)

    def __str__(self):
        return self.name
    
class Club(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    founded = models.DateField(null=True)
    logo = models.ImageField(upload_to='club_logos/', null=True)
    seasons = models.ManyToManyField(Season, through='ClubSeason')

    def __str__(self):
        return self.name
    
class ClubSeason(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return self.season.league.name + " " + str(self.season.start_date.year) + "-" + str(self.season.end_date.year) + " " + self.club.name
    
class Foot(models.Model):

    class FootEnum(models.TextChoices):
        LEFT = 'L', 'Left'
        RIGHT = 'R', 'Right'
        BOTH = 'B', 'Both'
        UNKNOWN = 'U', 'Unknown'

    foot = models.CharField(max_length=1, choices=FootEnum.choices, default=FootEnum.UNKNOWN)

    def __str__(self):
        return self.foot
    
class Position(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    x = models.IntegerField(default=0, null=True)
    y = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.name
    
class Player(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    full_name = models.CharField(max_length=200, null=True)
    playing_name = models.CharField(max_length=200, null=True)
    birth_date = models.DateField(null=True)
    height = models.IntegerField(default=0, null=True)
    foot = models.ForeignKey(Foot, on_delete=models.CASCADE)
    primary_position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="primary_position")
    secundary_positions = models.ManyToManyField(Position, through='PlayerPosition', related_name="secundary_positions")
    primary_nation = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="primary_nation")
    secundary_nations = models.ManyToManyField(Country, through='PlayerNations', related_name="secundary_nations")
    city_of_birth = models.ForeignKey(City, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    at_club_since = models.DateField(null=True)
    contract_until = models.DateField(null=True)
    contract_start = models.DateField(null=True)
    image_url = models.CharField(max_length=200, null=True)
    caps = models.IntegerField(default=0, null=True)
    international_goals = models.IntegerField(default=0, null=True)
    value = models.IntegerField(default=0, null=True)
    shirt_number = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    
class PlayerPosition(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.player.first_name + " " + self.player.last_name + " " + self.position.name
    
class PlayerNations(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.player.first_name + " " + self.player.last_name + " " + self.country.name
    
class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    transfer_fee = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.player.first_name + " " + self.player.last_name + " " + self.club.name + " " + str(self.date.year) + "-" + str(self.date.month) + "-" + str(self.date.day) + " " + str(self.transfer_fee)
    
class Formation(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    positions = models.ManyToManyField(Position, through='FormationPosition')

    def __str__(self):
        return self.name
    
class FormationPosition(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.formation.name + " " + self.position.name
    
class MatchLineup(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    shirt_number = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.player.first_name + " " + self.player.last_name + " " + self.club.name + " " + self.match.home_club.name + " " + self.match.away_club.name + " " + str(self.match.date.year) + "-" + str(self.match.date.month) + "-" + str(self.match.date.day) + " " + self.match.stadium.name + " " + self.match.competition.name
    
class MatchBenched(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    shirt_number = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.player.first_name + " " + self.player.last_name + " " + self.club.name + " " + self.match.home_club.name + " " + self.match.away_club.name + " " + str(self.match.date.year) + "-" + str(self.match.date.month) + "-" + str(self.match.date.day) + " " + self.match.stadium.name + " " + self.match.competition.name
    
class Match(models.Model):
    home_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="home_club")
    away_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="away_club")
    date = models.DateField(null=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    lineup = models.ManyToManyField('MatchLineup', related_name="lineup")
    benched = models.ManyToManyField('MatchBenched', related_name="benched")
    subs = models.ManyToManyField('Substitution', related_name="subs")
    cards = models.ManyToManyField('Card', related_name="cards")
    goals = models.ManyToManyField('Goal', related_name="goals")
    assists = models.ManyToManyField('Assist', related_name="assists")
    round_number = models.IntegerField(default=0, null=True)
    spectators = models.IntegerField(default=0, null=True)
    home_formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name="home_formation")
    away_formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name="away_formation")

    def __str__(self):
        return self.home_club.name + " " + self.away_club.name + " " + str(self.home_goals) + "-" + str(self.away_goals) + " " + str(self.date.year) + "-" + str(self.date.month) + "-" + str(self.date.day) + " " + self.stadium.name + " " + self.competition.name
    
class Assist(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    minute = models.IntegerField(default=0, null=True)
    extra_time = models.IntegerField(default=0, null=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    goal = models.ForeignKey('Goal', on_delete=models.CASCADE)

    def __str__(self):
        return self.player.first_name + " " + self.player.last_name + " " + self.club.name + " " + str(self.date.year) + "-" + str(self.date.month)
    
class Goal(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    minute = models.IntegerField(default=0, null=True)
    extra_time = models.IntegerField(default=0, null=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):
        return self.player.first_name + " " + self.player.last_name + " " + self.club.name + " " + str(self.date.year) + "-" + str(self.date.month) + "-" + str(self.date.day) + " " + str(self.minute) + " " + self.against.name + " " + self.stadium.name + " " + self.competition.name
    
class Substitution(models.Model):
    class ReasonEnum(models.TextChoices):
        INJURY = 'I', 'Injury'
        TACTICAL = 'T', 'Tactical'
        YELLOW_CARD = 'Y', 'Yellow Card'
        UNKNOWN = 'U', 'Unknown'
    
    player_in = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player_in")
    player_out = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player_out")
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    minute = models.IntegerField(default=0, null=True)
    extra_time = models.IntegerField(default=0, null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    reason = models.CharField(max_length=1, choices=ReasonEnum.choices, default=ReasonEnum.UNKNOWN)

    def __str__(self):
        return self.player_in.first_name + " " + self.player_in.last_name + " " + self.player_out.first_name + " " + self.player_out.last_name + " " + self.club.name + " " + self.match.home_club.name + " " + self.match.away_club.name + " " + str(self.match.date.year) + "-" + str(self.match.date.month) + "-" + str(self.match.date.day) + " " + self.match.stadium.name + " " + self.match.competition.name
    
class Card(models.Model):
    
    class CardEnum(models.TextChoices):
        YELLOW = 'Y', 'Yellow'
        RED = 'R', 'Red'
        SECOND_YELLOW = 'S', 'Second Yellow'

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    minute = models.IntegerField(default=0, null=True)
    extra_time = models.IntegerField(default=0, null=True)
    card = models.CharField(max_length=1, choices=CardEnum.choices, default=CardEnum.YELLOW)

    def __str__(self):
        return self.player.first_name + " " + self.player.last_name + " " + self.club.name + " " + self.match.home_club.name + " " + self.match.away_club.name + " " + str(self.match.date.year) + "-" + str(self.match.date.month) + "-" + str(self.match.date.day) + " " + self.match.stadium.name + " " + self.match.competition.name