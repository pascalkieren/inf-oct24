from otree.api import *
import itertools
import math

doc = """
Your app description
"""
def validate_one_decimal(value):
    # Check if the value has more than one decimal place
    if round(value, 1) != value:
        raise ValidationError('The value must have only one decimal place.')

def creating_session(subsession):
    treatments = list(itertools.product([1, 2, 3,4,5], [1, 2]))
    treatment_cycle = itertools.cycle(treatments)
    for player in subsession.get_players():
        situation, treatment = next(treatment_cycle)
        player.situation = situation
        player.treatment = treatment
        print(f"Player {player.id_in_group} assigned to situation {player.situation}, treatment {player.treatment}")


class C(BaseConstants):
    NAME_IN_URL = 'infexp'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 20

    baseline_label1 = 'the rate of inflation will be 12% or higher'
    baseline_label2 = 'the rate of inflation will be between 8% and 12%'
    baseline_label3 = 'the rate of inflation will be between 4% and 8%'
    baseline_label4 = 'the rate of inflation will be between 2% and 4%'
    baseline_label5 = 'the rate of inflation will be between 0% and 2%'
    baseline_label6 = 'the rate of deflation (opposite of inflation) will be between 0% and 2%'
    baseline_label7 = 'the rate of deflation (opposite of inflation) will be between 2% and 4%'
    baseline_label8 = 'the rate of deflation (opposite of inflation) will be between 4% and 8%'
    baseline_label9 = 'the rate of deflation (opposite of inflation) will be between 8% and 12%'
    baseline_label10 = 'the rate of deflation (opposite of inflation) will be 12% or higher'

    income_label1 = 'Decrease'
    income_label2 = 'Stay about the same'
    income_label3 = 'Increase'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # für alle treatments
    round_number_new = models.IntegerField()
    treatment = models.IntegerField()
    last_round_q25 = models.IntegerField()
    situation = models.IntegerField()
    median_check = models.FloatField()
    median_deflation_check = models.FloatField()
    sanity_median = models.IntegerField(choices=[
        [1, 'Agree'],
        [2, 'Rather higher'],
        [3, 'Rather lower']
    ])
    sanity_deflation = models.IntegerField(choices=[
        [1, 'Agree'],
        [2, 'Rather higher'],
        [3, 'Rather lower']
    ])

    # zählen für 2-step und endogenous method
    first_min_expectation = models.FloatField()
    first_max_expectation = models.FloatField()

    def error_message(self, values):
        min_expectation = values['first_min_expectation']
        max_expectation = values['first_max_expectation']

        if round(min_expectation, 1) != min_expectation:
            return 'Minimum expectation must have only one decimal place.'
        if round(max_expectation, 1) != max_expectation:
            return 'Maximum expectation must have only one decimal place.'

    bisection_upper = models.BooleanField(label="", initial=False)
    bisection_lower = models.BooleanField(label="", initial=False)

    # 2-step method
    stop1 = models.BooleanField(initial=True)
    stop2 = models.BooleanField(initial=True)
    stop3 = models.BooleanField(initial=True)
    min_expectation = models.FloatField(label="", blank=True, min=(-300))
    final_min_expectation = models.FloatField(label="", blank=True)
    max_expectation = models.FloatField(label="", blank=True, max=300)
    final_max_expectation = models.FloatField(label="", blank=True)
    first_min_expectation_q25 = models.FloatField()
    first_max_expectation_q25 = models.FloatField()
    min_expectation_q25 = models.FloatField()
    final_min_expectation_q25 = models.FloatField(label="", blank=True)
    max_expectation_q25 = models.FloatField()
    final_max_expectation_q25 = models.FloatField(label="", blank=True)
    first_min_expectation_q75 = models.FloatField()
    first_max_expectation_q75 = models.FloatField()
    min_expectation_q75 = models.FloatField()
    final_min_expectation_q75 = models.FloatField(label="", blank=True)
    max_expectation_q75 = models.FloatField()
    final_max_expectation_q75 = models.FloatField(label="", blank=True)
    confirmation = models.BooleanField(label="", blank=True)
    bisection = models.BooleanField(label="", blank=True)
    midpoint = models.FloatField(label="")
    midpoint_q25 = models.FloatField(label="")
    midpoint_q75 = models.FloatField(label="")
    final_midpoint = models.FloatField()
    final_midpoint_q25 = models.FloatField()
    final_midpoint_q75 = models.FloatField()

    prolific = models.StringField(
        label="Please enter your Prolific ID:"
    )
    pointprog = models.FloatField(
        label="", blank=True, min=-100, max=100)
    def error_message(self, values):
        pointprog = values['first_min_expectation']
        max_expectation = values['first_max_expectation']

        if round(pointprog, 1) != pointprog:
            return 'Minimum expectation must have only one decimal place.'

    # treatment: endogenous method

    range = models.FloatField(initial=0)

    range_q25 = models.FloatField(initial=0)
    range_q75 = models.FloatField(initial=0)
    round_number_q25 = models.FloatField(initial=1)

    counting = models.IntegerField(initial=1)

    # treatment_bins
    q1_org_bin1 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin2 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin3 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin4 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin5 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin6 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin7 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin8 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin9 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin10 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin11 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q1_org_bin1_by_player = models.BooleanField(initial=False)
    q1_org_bin2_by_player = models.BooleanField(initial=False)
    q1_org_bin3_by_player = models.BooleanField(initial=False)
    q1_org_bin4_by_player = models.BooleanField(initial=False)
    q1_org_bin5_by_player = models.BooleanField(initial=False)
    q1_org_bin6_by_player = models.BooleanField(initial=False)
    q1_org_bin7_by_player = models.BooleanField(initial=False)
    q1_org_bin8_by_player = models.BooleanField(initial=False)
    q1_org_bin9_by_player = models.BooleanField(initial=False)
    q1_org_bin10_by_player = models.BooleanField(initial=False)
    q1_org_bin11_by_player = models.BooleanField(initial=False)
    q1_org_bin12_by_player = models.BooleanField(initial=False)
    q1_org_bin13_by_player = models.BooleanField(initial=False)
    q1_org_bin14_by_player = models.BooleanField(initial=False)
    # Sum of the bins answered by player
    q1_org_sum_by_player = models.IntegerField(initial=0)

    q1_org_sum = models.IntegerField(initial=0, blank=True)
    q1_org_sum_100 = models.BooleanField(initial=False, blank=True)
    q1_org_sum_0 = models.BooleanField(initial=False, blank=True)

    q3_org_sum = models.IntegerField(initial=0, blank=True)
    # Question 1: Fields for the sum of the bins (if estimates less/more than 100 in sum)
    q1_rep_sum = models.IntegerField(initial=0, blank=True)
    q1_rep_sum_100 = models.BooleanField(initial=False, blank=True)
    q1_rep_sum_0 = models.BooleanField(initial=False, blank=True)
    saw_q1_no_response_error = models.BooleanField(initial=False, required=False)
    answered_q1 = models.BooleanField(initial=False, required=False)

    # adding all bin variables for treatment four

    q4_org_bin1 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin2 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin3 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin4 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin5 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin6 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin7 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin8 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin9 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin10 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin11 = models.IntegerField(min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    q4_org_bin1_by_player = models.BooleanField(initial=False)
    q4_org_bin2_by_player = models.BooleanField(initial=False)
    q4_org_bin3_by_player = models.BooleanField(initial=False)
    q4_org_bin4_by_player = models.BooleanField(initial=False)
    q4_org_bin5_by_player = models.BooleanField(initial=False)
    q4_org_bin6_by_player = models.BooleanField(initial=False)
    q4_org_bin7_by_player = models.BooleanField(initial=False)
    q4_org_bin8_by_player = models.BooleanField(initial=False)
    q4_org_bin9_by_player = models.BooleanField(initial=False)
    q4_org_bin10_by_player = models.BooleanField(initial=False)
    q4_org_bin11_by_player = models.BooleanField(initial=False)
    q4_org_bin12_by_player = models.BooleanField(initial=False)
    q4_org_bin13_by_player = models.BooleanField(initial=False)
    q4_org_bin14_by_player = models.BooleanField(initial=False)
    # Sum of the bins answered by player
    q4_org_sum_by_player = models.IntegerField(initial=0)

    q4_org_sum = models.IntegerField(initial=0, blank=True)
    q4_org_sum_100 = models.BooleanField(initial=False, blank=True)
    q4_org_sum_0 = models.BooleanField(initial=False, blank=True)

    # Question 4: Fields for the sum of the bins (if estimates less/more than 100 in sum)
    q4_rep_sum = models.IntegerField(initial=0, blank=True)
    q4_rep_sum_100 = models.BooleanField(initial=False, blank=True)
    q4_rep_sum_0 = models.BooleanField(initial=False, blank=True)
    saw_q4_no_response_error = models.BooleanField(initial=False, required=False)
    answered_q4 = models.BooleanField(initial=False, required=False)

    # demographic questions
    age = models.IntegerField(label="Age:")
    gender = models.IntegerField(label="Gender:", choices=[[-1, "Female"], [1, "Male"], [2, "Diverse"],
                                                           [3, "Prefer not to say"]],
                                 widget=widgets.RadioSelect)
    female = models.BooleanField(blank=True)
    income = models.IntegerField(
        label="",
        choices=[[1, "Less than $1,000"], [2, "$1,000 to $1,999"], [3, "$2,000 to $2,999"], [4, "$3,000 to $3,999"],
                 [5, "$4,000 to $4,999"], [6, "$5,000 to $5,999"], [7, "$6,000 to $6,999"], [8, "$7,000 to $7,999"],
                 [9, "$8,000 to $9,999"], [10, "$10,000 to $11,999"], [11, "$12,000 or more"]])
    education = models.IntegerField(label="What is your highest level of educational attainment? ",
                                    choices=[[-1, "Prefer not to answer"], [1, "Less than high school diploma"],
                                             [2, "High school diploma"],
                                             [3, "Some college no degree"], [4, "Associate's degree occupational"],
                                             [5, "Associate's degree academic"], [6, "Bachelor's degree"],
                                             [7, "Master's degree"], [8, "Professional degree"],
                                             [9, "Doctoral degree"]],
                                    widget=widgets.RadioSelect)

    income1 = models.IntegerField(label="", min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    income2 = models.IntegerField(label="", min=0, max=100, blank=True, null=True, widget=widgets.TextInput())
    income3 = models.IntegerField(label="", min=0, max=100, blank=True, null=True, widget=widgets.TextInput())

    income1_by_player = models.BooleanField(initial=False)
    income2_by_player = models.BooleanField(initial=False)
    income3_by_player = models.BooleanField(initial=False)

    income_org_sum_by_player = models.IntegerField(initial=0)

    income_org_sum = models.IntegerField(initial=0, blank=True)
    income_org_sum_100 = models.BooleanField(initial=0, blank=True)
    income_org_sum_0 = models.BooleanField(initial=0, blank=True)

    # Question 1: Fields for the sum of the bins (if estimates less/more than 100 in sum)
    q3_rep_sum = models.IntegerField(initial=0, blank=True)
    q3_rep_sum_100 = models.BooleanField(initial=False, blank=True)
    q3_rep_sum_0 = models.BooleanField(initial=False, blank=True)
    saw_q3_no_response_error = models.BooleanField(initial=False, required=False)
    answered_q3 = models.BooleanField(initial=False, required=False)

    spending1 = models.FloatField(label="Major purchases (e.g. car, furniture, electrical appliances, etc.)")
    spending2 = models.FloatField(
        label="Essential goods (e.g. food and beverages, non-food items such as cleaning products or similar)")
    spending3 = models.FloatField(label="Clothing and footwear")
    spending4 = models.FloatField(label="Entertainment/recreation (e.g. restaurant visits, cultural events, gym)")
    spending5 = models.FloatField(
        label="Mobility (e.g. fuel, car loans and running costs, bus and train tickets)")
    spending6 = models.FloatField(
        label="Services (e.g. hairdresser, childcare, medical costs)")
    spending7 = models.FloatField(
        label="Travel, holidays")
    spending8 = models.FloatField(
        label="Housing costs (e.g. rent, mortgage, ancillary costs)")
    spending9 = models.FloatField(
        label="Financial reserves")

    major_purchases = models.IntegerField(
        label="Major purchases (e.g. car, furniture, electrical appliances, etc.)",
        choices=[
            [1, 'Plan to spend more'],
            [2, 'Plan to spend roughly the same'],
            [3, 'Plan to spend less']
    ])

    essential_goods = models.IntegerField(
        label="Essential goods (e.g. food and beverages, non-food items such as cleaning products or similar)",
        choices=[
            [1, 'Plan to spend more'],
            [2, 'Plan to spend roughly the same'],
            [3, 'Plan to spend less']
    ])

    clothing_and_footwear = models.IntegerField(
        label="Clothing and footwear",
        choices=[
            [1, 'Plan to spend more'],
            [2, 'Plan to spend roughly the same'],
            [3, 'Plan to spend less']
    ])

    entertainment_recreation = models.IntegerField(
        label="Entertainment/recreation (e.g. restaurant visits, cultural events, gym)",
        choices=[
            [1, 'Plan to spend more'],
            [2, 'Plan to spend roughly the same'],
            [3, 'Plan to spend less']
    ])

    mobility = models.IntegerField(
        label="Mobility (e.g. fuel, car loans and running costs, bus and train tickets)",
        choices=[
            [1, 'Plan to spend more'],
            [2, 'Plan to spend roughly the same'],
            [3, 'Plan to spend less']
    ])

    services = models.IntegerField(
        label="Services (e.g. hairdresser, childcare, medical costs)",
        choices=[
            [1, 'Plan to spend more'],
            [2, 'Plan to spend roughly the same'],
            [3, 'Plan to spend less'],
    ])

    travel_holidays = models.IntegerField(
        label="Travel, holidays",
        choices=[
            [1, 'Plan to spend more'],
            [2, 'Plan to spend roughly the same'],
            [3, 'Plan to spend less'],
    ])

    housing_costs = models.IntegerField(
        label="Housing costs (e.g. rent, mortgage, ancillary costs)",
        choices=[
            [1, 'Plan to spend more'],
            [2, 'Plan to spend roughly the same'],
            [3, 'Plan to spend less'],
    ])

    financial_reserves = models.IntegerField(
        label="Financial reserves",
        choices=[
            [1, 'Plan to spend more'],
            [2, 'Plan to spend roughly the same'],
            [3, 'Plan to spend less'],
    ])

    good_real_estate = models.IntegerField(
        label="Is this a good time or a bad time to invest in real estate in your city?",
        choices=[
            [1, 'Very bad'],
            [2, 'Bad'],
            [3, 'Neither good or bad'],
            [4, 'Good'],
            [5, 'Very good'],
    ])

    good_car = models.IntegerField(
        label="Is this a good time or a bad time to buy a car?",
        choices=[
            [1, 'Very bad'],
            [2, 'Bad'],
            [3, 'Neither good or bad'],
            [4, 'Good'],
            [5, 'Very good'],
    ])

    good_durable_goods = models.IntegerField(
        label="Is this a good time or a bad time to buy durable goods like electronics, mobile phones, home appliances?",
        choices=[
            [1, 'Very bad'],
            [2, 'Bad'],
            [3, 'Neither good or bad'],
            [4, 'Good'],
            [5, 'Very good']],
    )

    good_loans1 = models.IntegerField(
        label="In the next 12 months, do you plan to apply for new loans (such as an auto-loan, home-based loan, personal loan, etc.) or request a credit limit increase on your credit card?",
        choices=[[1, 'Yes'], [2, 'No'],
    ])

    good_loans2 = models.IntegerField(
        label="How difficult do you believe it is to obtain a new loan/credit at present?",
        choices=[
            [1, 'Very easy'],
            [2, 'Easy'],
            [3, 'Neutral'],
            [4, 'Difficult'],
            [5, 'Very difficult']],
        )


    question_dif = models.IntegerField(
        label="How easy or hard was it to answer the questions so far? Please select one answer.",
        choices=[[1, "Very difficult"], [2, "Somewhat difficult"], [3, "Neither difficult nor easy"],
                 [4, "Somewhat easy"], [5, "Very easy"]],
        widget=widgets.RadioSelect)
    question_length = models.IntegerField(
        label="How did you find the length of the survey so far?",
        choices=[[1, "Far too long"], [2, "Somewhat too Long"], [3, "Just right"],
                 [4, "Somewhat too short"], [5, "Far too short"]],
        widget=widgets.RadioSelect)

    unemployment = models.IntegerField(
        label="The unemployment rate in the US:",
        choices=[
            [1, 'Decrease Significantly'],
            [2, 'Decrease Slightly'],
            [3, 'Stay roughly the same'],
            [4, 'Increase Slightly'],
            [5, 'Increase Significantly']],
    )

    rent = models.IntegerField(
        label="Rents in your area:",
        choices=[
            [1, 'Decrease Significantly'],
            [2, 'Decrease Slightly'],
            [3, 'Stay roughly the same'],
            [4, 'Increase Slightly'],
            [5, 'Increase Significantly']],
    )

    lending = models.IntegerField(
        label="Lending rates:",
        choices=[
            [1, 'Decrease Significantly'],
            [2, 'Decrease Slightly'],
            [3, 'Stay roughly the same'],
            [4, 'Increase Slightly'],
            [5, 'Increase Significantly']])

    interest = models.IntegerField(
        label="The interest rates on savings accounts:",
        choices=[
            [1, 'Decrease Significantly'],
            [2, 'Decrease Slightly'],
            [3, 'Stay roughly the same'],
            [4, 'Increase Slightly'],
            [5, 'Increase Significantly']],
    )

    inflation = models.IntegerField(
        label="The inflation rate:",
        choices=[
            [1, 'Decrease Significantly'],
            [2, 'Decrease Slightly'],
            [3, 'Stay roughly the same'],
            [4, 'Increase Slightly'],
            [5, 'Increase Significantly']],
    )

    property = models.IntegerField(
        label="Property prices in your area:",
        choices=[
            [1, 'Decrease Significantly'],
            [2, 'Decrease Slightly'],
            [3, 'Stay roughly the same'],
            [4, 'Increase Slightly'],
            [5, 'Increase Significantly']],
    )

    survey_complete = models.BooleanField(Initial=False)


# FUNCTIONS
def calculate_deflation_probability(player):
    # Retrieve the values from the relevant rounds
    min_expectation = float(player.in_round(1).first_min_expectation)
    max_expectation = player.in_round(1).first_max_expectation

    # Initialize deflation probability
    deflation_prob = 0

    # Case 1: If min is greater than or equal to zero, no deflation probability
    if min_expectation >= 0:
        return 0
    final_midpoint = None
    for round_number in range(player.round_number, 0, -1):  # Loop backwards from current round to round 1
        try:
            final_midpoint = player.in_round(round_number).field_maybe_none('final_midpoint')
            if final_midpoint is not None:
                break
        except AttributeError:
            continue

    final_midpoint_q25 = None
    for round_number in range(player.round_number, 0, -1):  # Loop backwards from current round to round 1
        try:
            final_midpoint_q25 = player.in_round(round_number).field_maybe_none('final_midpoint_q25')
            if final_midpoint_q25 is not None:
                break
        except AttributeError:
            continue
    midpoint_q75 = None
    for round_number in range(player.round_number, 0, -1):  # Loop backwards from current round to round 1
        try:
            midpoint_q75 = player.in_round(round_number).field_maybe_none('final_midpoint_q75')
            if midpoint_q75 is not None:
                break
        except AttributeError:
            continue
    # Ensure final_midpoint_q25 was found
    if final_midpoint_q25 is None:
        raise ValueError("final_midpoint_q25 is not defined in any previous rounds")

    # Case 2: Check if q25 is less than zero
    if final_midpoint_q25 < 0:
        deflation_prob += 25
    elif min_expectation < 0:
        # If q25 is greater than zero and min is less than zero, calculate partial probability
        deflation_prob += (0 - min_expectation) / (final_midpoint_q25 - min_expectation) * 25

    # Case 3: Check if q50 (final_midpoint) is less than zero
    if final_midpoint < 0:
        deflation_prob += 25
    elif final_midpoint_q25 < 0:
        # If q50 is greater than zero and q25 is less than zero, calculate partial probability
        deflation_prob += (0 - final_midpoint_q25) / (final_midpoint - final_midpoint_q25) * 25

    # Case 4: Check if q75 is less than zero
    if midpoint_q75 < 0:
        deflation_prob += 25
    elif final_midpoint < 0:
        # If q75 is greater than zero and q50 is less than zero, calculate partial probability
        deflation_prob += (0 - final_midpoint) / (midpoint_q75 - final_midpoint) * 25

    # Case 5: Check if max is less than zero
    if max_expectation < 0:
        deflation_prob += 25
    elif midpoint_q75 < 0:
        # If max is greater than zero and q75 is less than zero, calculate partial probability
        deflation_prob += (0 - midpoint_q75) / (max_expectation - midpoint_q75) * 25

    return deflation_prob

def sum_bins(b_list):
    total = 0
    for b in b_list:
        total += b
    return total


def sum_bins4(b4_list):
    total4 = 0
    for b4 in b4_list:
        total4 += b4
    return total4


def sum_incomes(i_list):
    total_i = 0
    for i in i_list:
        total_i += i
    return total_i


def calculate_variables(pointprog):
    pointprogplus8 = pointprog + 8
    pointprogplus4 = pointprog + 4
    pointprogminus2 = pointprog - 2
    pointprogminus4 = pointprog - 4
    pointprogplus2 = pointprog + 2
    pointprogplus12 = pointprog + 12


# PAGES
class Instructions(Page):
    form_model = "player"
    form_fields = ["prolific"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Point(Page):
    form_model = "player"
    form_fields = ["pointprog"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        if values['pointprog'] == None:
            return "Please answer the question."
        if values['pointprog'] < -100 or values['pointprog'] > 100:
            return "Please only enter values between -100 and 100."

class info_intro(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.situation in [1, 2,4,5]


class info_high(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.situation == 1


class info_low(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.situation == 2


class info_control(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.situation == 3

class info_mean(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.situation == 4

class info_uncertainty(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.situation == 5
class InflationsErwartung(Page):
    form_model = "player"
    form_fields = ["min_expectation", "max_expectation"]


    @staticmethod
    def is_displayed(player: Player):
        return player.situation in [1, 2, 3, 4, 5] and player.treatment == 1 and player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        if values['min_expectation'] is None or values['max_expectation'] is None:
            return "Please answer the question."
        if values['min_expectation'] < -100:
            return "Please only enter values between -100 and 100."
        elif values['max_expectation'] > 100:
            return "Please only enter values between -100 and 100."
        elif values['min_expectation'] > values['max_expectation']:
            return 'Your Minimum Inflation Expectation cannot be larger than your Maximum Inflation Expectation.'
        elif values['min_expectation'] == values['max_expectation']:
            return 'Minimum and maximum inflation expectations cannot be the same.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.range = player.max_expectation - player.min_expectation
        player.first_min_expectation = player.min_expectation
        player.first_max_expectation = player.max_expectation
        player.midpoint = (player.min_expectation + player.max_expectation) / 2
        if player.max_expectation - player.min_expectation > 3:
            player.stop1 = False
        #THIS IS NEW
        else:
            player.final_midpoint = player.midpoint
            player.range_q25 = player.final_midpoint - player.in_round(1).first_min_expectation
            player.range_q75 = player.in_round(1).first_max_expectation - player.final_midpoint
            if player.range_q25 <= 3:
                player.final_midpoint_q25 = (player.in_round(1).first_min_expectation + player.final_midpoint) / 2
                player.stop2 = True
            if player.range_q75 <= 3:
                player.final_midpoint_q75 = (player.in_round(1).first_max_expectation + player.final_midpoint) / 2
                player.stop3 = True


class InflationsErwartung2(Page):
    # Spieler werden in Runde 1 nach Inflationserwartung gefragt
    form_model = "player"
    form_fields = ["min_expectation", "max_expectation"]

    @staticmethod
    def is_displayed(player: Player):
        return  player.treatment == 1 and player.round_number == 1 and player.confirmation == False

    @staticmethod

    def vars_for_template(player: Player):
        return dict(
            confirmation=player.confirmation
        )

    @staticmethod
    def error_message(player: Player, values):
        if values['min_expectation'] < -100:
            return "Please only enter values between -100 and 100."
        elif values['max_expectation'] > 100:
            return "Please only enter values between -100 and 100."
        elif values['min_expectation'] == None:
            return "Please enter your inflation expectation."
        elif values['max_expectation'] == None:
            return "Please enter your inflation expectation."
        elif values['min_expectation'] > values['max_expectation']:
            return 'Your Minimum Inflation Expectation cannot be larger than your Maximum Inflation Expectation.'
        elif values['min_expectation'] == values['max_expectation']:
            return 'Minimum und maximum inflation expectation cannot be the same.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.first_min_expectation = player.min_expectation
        player.first_max_expectation = player.max_expectation
        player.range = player.max_expectation - player.min_expectation
        player.midpoint = (player.min_expectation + player.max_expectation) / 2
        if player.max_expectation - player.min_expectation > 3:
            player.stop1 = False
        #THIS IS NEW
        else:
            player.final_midpoint = player.midpoint
            player.range_q25 = player.final_midpoint - player.in_round(1).first_min_expectation
            player.range_q75 = player.in_round(1).first_max_expectation - player.final_midpoint
            if player.range_q25 <= 3:
                player.final_midpoint_q25 = (player.in_round(1).first_min_expectation + player.final_midpoint) / 2
                player.stop2 = True
            if player.range_q75 <= 3:
                player.final_midpoint_q75 = (player.in_round(1).first_max_expectation + player.final_midpoint) / 2
                player.stop3 = True


class Confirmation(Page):
    form_model = 'player'
    form_fields = ['confirmation']

    def is_displayed(player: Player):
        return player.situation in [1,2,3,4,5] and player.treatment == 1 and player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            min_expectation=player.in_round(1).min_expectation,
            max_expectation=player.in_round(1).max_expectation,
        )


class InstructionsP2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.treatment == 1) and player.round_number == 1 and player.in_round(
            1).range > 3


class Q25Screen(Page):

    @staticmethod
    def is_displayed(player: Player):
        return (player.treatment == 1) and player.stop1 == True and player.stop2 == False and player.range_q25 > 3


class Q75Screen(Page):

    @staticmethod
    def is_displayed(player: Player):
        return (player.treatment == 1) and player.stop1 == True and player.stop2 == True and player.stop3 == False and player.range_q75 > 3


# treatment 1

class Bisection1(Page):
    form_model = "player"
    form_fields = ["bisection"]

    @staticmethod
    def is_displayed(player: Player):
        return (player.treatment == 1) and player.in_round(1).range > 3 and player.round_number >= 1 and (player.stop1 == False or player.in_round(player.round_number - 1).stop1 == False)

    @staticmethod
    def error_message(player: Player, values):
        if values['bisection'] == None:
            return "Please choose an option."

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number == 1:
            return dict(
                min_expectation=player.in_round(1).first_min_expectation,
                max_expectation=player.in_round(1).first_max_expectation,
                mid_point=round(player.midpoint,2),
                counting = 1

            )
        else:
            return dict(
                min_expectation=player.in_round(1).first_min_expectation,
                max_expectation=player.in_round(1).first_max_expectation,
                mid_point=round(player.in_round(player.round_number-1).midpoint,2),
                max_expectation1 = player.in_round(player.round_number - 1).max_expectation,
                range = player.range,
                counting = player.in_round(player.round_number - 1).counting

            )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.round_number_new = player.round_number

        if player.round_number == 1:
            player.counting = 2
        else:
            player.counting = player.in_round(player.round_number - 1).counting + 1

        if player.bisection == True:
            player.bisection_lower = True
            player.bisection_upper = False

        else:
            player.bisection_upper = True
            player.bisection_lower = False

        if player.round_number == 1:
            if player.bisection:
                player.max_expectation = player.midpoint
                player.midpoint = (player.min_expectation + player.max_expectation) / 2
            else:
                player.min_expectation = player.midpoint
                player.midpoint = (player.min_expectation + player.max_expectation) / 2
        else:
            if player.bisection:
                player.max_expectation = player.in_round(player.round_number - 1).midpoint
                player.min_expectation = player.in_round(player.round_number - 1).min_expectation
                player.midpoint = (player.min_expectation + player.max_expectation) / 2
            else:
                player.min_expectation = player.in_round(player.round_number - 1).midpoint
                player.max_expectation = player.in_round(player.round_number - 1).max_expectation
                player.midpoint = (player.min_expectation + player.max_expectation) / 2

        player.range = player.max_expectation - player.min_expectation
        if player.range > 3:
            player.stop1 = False
        else:
            player.stop1 = True
            player.stop2 = False
            player.stop3 = False
            player.final_midpoint = player.midpoint
            player.counting = 1

            player.range_q25 = player.midpoint - player.in_round(1).first_min_expectation
            if player.range_q25 <= 3:
                player.final_midpoint_q25 = (player.in_round(1).first_min_expectation + player.final_midpoint) / 2
                player.stop2 = True
            else:
                player.first_min_expectation_q25 = player.in_round(1).first_min_expectation
                player.min_expectation_q25 = player.first_min_expectation_q25
                player.first_max_expectation_q25 = player.final_midpoint
                player.max_expectation_q25 = player.first_max_expectation_q25
                player.midpoint_q25 = (player.first_min_expectation_q25 + player.first_max_expectation_q25) / 2

            player.range_q75 = player.in_round(1).first_max_expectation - player.final_midpoint
            if player.range_q75 <= 3:
                player.final_midpoint_q75 = (player.in_round(1).first_max_expectation + player.final_midpoint) / 2
                player.stop3 = True
                player.min_expectation_q75 = player.in_round(1).first_max_expectation
                player.max_expectation_q75 = player.final_midpoint
                player.midpoint_q75 = (player.min_expectation_q75 + player.max_expectation_q75) / 2
            else:
                player.first_max_expectation_q75 = player.in_round(1).first_max_expectation
                player.first_min_expectation_q75 = player.final_midpoint
                player.min_expectation_q75 = player.first_min_expectation_q75
                player.max_expectation_q75 = player.first_max_expectation_q75
                player.midpoint_q75 = (player.first_min_expectation_q75 + player.first_max_expectation_q75) / 2




        #
        # if player.round_number == 1 and player.round_number != player.in_round(1).round_number_bi:
        #     player.counting += 1
        # elif player.round_number == player.in_round(1).round_number_bi:
        #     player.counting = 1
        # elif player.round_number == player.in_round(1).round_number_bi and player.round_number == 1:
        #     player.counting = 1
        # else:
        #     player.counting = player.in_round(player.round_number - 1).counting + 1


class Q25_1(Page):
    form_model = "player"
    form_fields = ["bisection"]

    @staticmethod
    def is_displayed(player: Player):
        return (player.treatment == 1) and player.round_number > 1 and player.in_round(
            player.round_number - 1).stop1 and not player.in_round(player.round_number - 1).stop2 and player.in_round(
            player.round_number - 1).range_q25 > 3

    @staticmethod
    def error_message(player: Player, values):
        if values['bisection'] is None:
            return "Please choose an option."

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            min_expectation=player.in_round(1).first_min_expectation,
            mid_point=round(player.in_round(player.round_number - 1).final_midpoint, 2),
            midpoint_q25=round(player.in_round(player.round_number - 1).midpoint_q25, 2),
            counting=player.in_round(player.round_number - 1).counting
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Initialize variables to ensure they are always defined
        player.round_number_new = player.round_number

        # Retain values from the previous round
        player.min_expectation_q75 = player.in_round(player.round_number - 1).min_expectation_q75
        player.max_expectation_q75 = player.in_round(player.round_number - 1).max_expectation_q75
        player.midpoint_q75 = player.in_round(player.round_number - 1).midpoint_q75
        player.range_q75 = player.max_expectation_q75 - player.min_expectation_q75
        player.final_midpoint = player.in_round(player.round_number - 1).final_midpoint

        # Set bisection flags
        if player.bisection:
            player.bisection_lower = True
            player.bisection_upper = False
        else:
            player.bisection_upper = True
            player.bisection_lower = False

        player.counting = player.in_round(player.round_number - 1).counting + 1

        # Calculate new midpoint and range for Q25
        if player.bisection:
            player.max_expectation_q25 = player.in_round(player.round_number - 1).midpoint_q25
            player.min_expectation_q25 = player.in_round(player.round_number - 1).min_expectation_q25
        else:
            player.min_expectation_q25 = player.in_round(player.round_number - 1).midpoint_q25
            player.max_expectation_q25 = player.in_round(player.round_number - 1).max_expectation_q25

        player.midpoint_q25 = (player.min_expectation_q25 + player.max_expectation_q25) / 2
        player.range_q25 = player.max_expectation_q25 - player.min_expectation_q25

        # Handle the median deflation check
        if player.in_round(1).first_min_expectation >= 0:
            player.median_deflation_check = 0

        # Check if range_q25 is sufficiently small to finalize the midpoint
        if player.range_q25 > 3:
            player.stop2 = False
        else:
            player.stop2 = True
            player.stop3 = False
            player.final_midpoint_q25 = player.midpoint_q25
            player.last_round_q25 = player.round_number

            print(f"[DEBUG] Q25_1 - Final midpoint_q25: {player.final_midpoint_q25} on round {player.last_round_q25}")
            player.counting = 1



            # if player.bisection == True:
            #     player.final_max_expectation_q25 = player.midpoint
            #     player.final_min_expectation_q25 = player.min_expectation_q25
            # else:
            #     player.final_min_expectation_q25 = player.midpoint
            #     player.final_max_expectation_q25 = player.max_expectation_q25
            # player.final_midpoint_q25 = (player.final_min_expectation_q25 + player.final_max_expectation_q25) / 2


class Q75_1(Page):
    form_model = "player"
    form_fields = ["bisection"]

    @staticmethod
    def is_displayed(player: Player):
        return (player.treatment == 1 ) and player.round_number > 1 and player.in_round(player.round_number - 1).stop1 == True and player.in_round(player.round_number - 1).stop2 == True and player.in_round(player.round_number - 1).stop3 == False and player.in_round(player.round_number - 1).range_q75 > 3

    @staticmethod
    def error_message(player: Player, values):
        if values['bisection'] == None:
            return "Please choose an option."

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'min_expectation': player.in_round(1).first_min_expectation,
            'max_expectation': player.in_round(1).first_max_expectation,
            'mid_point': round(player.in_round(player.round_number - 1).final_midpoint, 2),
            'midpoint_q75': round(player.in_round(player.round_number - 1).midpoint_q75, 2),
            'counting': player.in_round(player.round_number - 1).counting,
            'stop1': player.in_round(player.round_number - 1).stop1,
            'stop2': player.in_round(player.round_number - 1).stop2,
            'stop3': player.in_round(player.round_number - 1).stop3,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.round_number_new = player.round_number

        player.counting = player.in_round(player.round_number - 1).counting + 1

        player.final_midpoint = player.in_round(player.round_number - 1).final_midpoint

        if player.bisection == True:
            player.bisection_lower = True
            player.bisection_upper = False
        else:
            player.bisection_upper = True
            player.bisection_lower = False

        if player.bisection:
            player.max_expectation_q75 = player.in_round(player.round_number - 1).midpoint_q75
            player.min_expectation_q75 = player.in_round(player.round_number - 1).min_expectation_q75
            player.midpoint_q75 = (player.min_expectation_q75 + player.max_expectation_q75) / 2
        else:
            player.min_expectation_q75 = player.in_round(player.round_number - 1).midpoint_q75
            player.max_expectation_q75 = player.in_round(player.round_number - 1).max_expectation_q75
            player.midpoint_q75 = (player.min_expectation_q75 + player.max_expectation_q75) / 2

        player.range_q75 = player.max_expectation_q75 - player.min_expectation_q75
        if player.range_q75 > 3:
            player.stop3 = False
        else:
            player.final_midpoint_q75 = player.midpoint_q75
            player.median_check = player.final_midpoint

        player.counting = player.in_round(player.round_number - 1).counting + 1



# bins

class Bins(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 2 and player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        fields = [f'q1_org_bin{i}' for i in range(1, 12)]
        totals = 0
        for field in fields:
            value = values.get(field, 0)
            if not value:
                value = 0
            totals += int(value)

        if totals != 100:
            return 'Please make sure the values add to 100'

    @staticmethod
    def get_form_fields(player):
        return [f'q1_org_bin{i}' for i in range(1, 11)]

    @staticmethod
    def vars_for_template(player: Player):
        fields = [f'q1_org_bin{i}' for i in range(1, 11)]
        labels = [getattr(C, f'baseline_label{i}') for i in range(1, 11)]
        combined = zip(labels, fields)
        return dict(combined=combined)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.saw_q1_no_response_error = True
        # First try if the bins are empty. If yes, replace with 0
        for i in range(1, 11):
            try:
                getattr(player, 'q1_org_bin' + str(i))
                exec("{0} = {1}".format('player.q1_org_bin' + str(i) + '_by_player', True))
            except TypeError:
                exec("{0} = {1}".format('player.q1_org_bin' + str(i), 0))
                # {0} and {1} are indices to be replaced by the arguments of .format

        bins = [getattr(player, f'q1_org_bin{i}') for i in range(1, 11)]
        player.q1_org_sum = sum_bins(bins)
        bins_by_player = [getattr(player, f'q1_org_bin{i}_by_player') for i in range(1, 11)]
        player.q1_org_sum_by_player = sum_bins(bins_by_player)

        # Case 1: Beliefs add up to 100
        if player.q1_org_sum == 100:
            player.q1_org_sum_100 = True
            player.answered_q1 = True

        # Case 2: Beliefs add up to 0 (i.e. participant didn't enter anything)
        # In this case set them to none again to restart the density question
        if player.q1_org_sum == 0:
            player.q1_org_sum_0 = True
            for i in range(1, 11):
                exec("{0} = {1}".format('player.q1_org_bin' + str(i), None))

        if timeout_happened:
            player.has_timeout = True
            player.session.dropout_treatments.append(player.treatment)

        if (player.treatment == 2) and (player.round_number == 1):
            #bin_ranges = [(12, 16), (8, 12), (4, 8), (2, 4), (0, 2), (-2, 0), (-4, -2), (-8, -4), (-12, -8), (-16, -12)]
            #bins = [
            #    player.q1_org_bin1, player.q1_org_bin2, player.q1_org_bin3, player.q1_org_bin4, player.q1_org_bin5,
            #    player.q1_org_bin6, player.q1_org_bin7, player.q1_org_bin8, player.q1_org_bin9, player.q1_org_bin10,
            #]
            #THIS IS NEW
            bin_ranges = [(-16, -12), (-12, -8), (-8, -4), (-4, -2), (-2, 0), (0, 2), (2, 4), (4, 8), (8, 12), (12, 16)]
            bins = [
                player.q1_org_bin10, player.q1_org_bin9, player.q1_org_bin8, player.q1_org_bin7, player.q1_org_bin6,
                player.q1_org_bin5, player.q1_org_bin4, player.q1_org_bin3, player.q1_org_bin2, player.q1_org_bin1,
            ]


            # Calculate median_check for the bins
            cumulative = 0
            median_bin = None
            selected_median = None

            for i, bin_value in enumerate(bins):
                if bin_value is None:
                    bin_value = 0
                cumulative += bin_value

                if cumulative >= 50:
                    median_bin = i

                    # If the cumulative hits exactly 50% at this bin, take the upper bound of this bin
                    if cumulative == 50:
                        for j in range(i + 1, len(bins)):
                            if bins[j] is not None and bins[j] > 0:
                                #selected_median = bin_ranges[j][1]
                                #THIS IS NEW
                                selected_median = bin_ranges[i][1]
                                break
                        # If all subsequent bins are empty, use the current bin's upper bound
                        if selected_median is None:
                            selected_median = bin_ranges[i][1]
                    else:
                        lower_bound, upper_bound = bin_ranges[median_bin]
                        range_size = upper_bound - lower_bound
                        missing_to_50 = 50 - (cumulative - bins[median_bin])
                        selected_median = lower_bound + (range_size / bin_value) * missing_to_50
                    break

            if selected_median is not None:
                print(f"Cumulative: {cumulative}")
                print(f"Selected median: {selected_median}")

                # Store median_check in participant's session data
                player.participant.vars['median_check'] = selected_median
            else:
                raise ValueError("The sum of bin values does not reach 50%.")

            deflation_bins = bins[:5]
            cumulative_deflation = sum(filter(None, deflation_bins))
            median_deflation_check = cumulative_deflation if cumulative_deflation > 0 else 0

            # Store median_deflation_check in participant's session data
            player.participant.vars['median_deflation_check'] = median_deflation_check
# demographics

class Demo7(Page):
    form_model = "player"
    form_fields = ["question_dif", "question_length"]

    @staticmethod
    def is_displayed(player: Player):
        return player.stop1 and player.stop2 and player.stop3


class Demo1(Page):
    form_model = "player"
    form_fields = ["gender", "age"]

    @staticmethod
    def is_displayed(player: Player):
        return player.stop1 and player.stop2 and player.stop3


class Demo2(Page):
    form_model = "player"
    form_fields = ["income", "education"]

    @staticmethod
    def is_displayed(player: Player):
        return player.stop1 and player.stop2 and player.stop3


class Demo3(Page):
    form_model = "player"

#    @staticmethod
#    def error_message(player: Player, values):
#        total_i = sum(values.get(f'income{i}', 0) for i in range(1, 4))
#        if total_i != 100:
#            return 'Please make sure the values add up to 100.'

    @staticmethod
    def error_message(player: Player, values):
        fields = [f'income{i}' for i in range(1, 4)]
        totals = 0
        for field in fields:
            value = values.get(field, 0)
            if not value:
                value = 0
            totals += int(value)

        if totals != 100:
            return 'Please make sure the values add to 100'


    @staticmethod
    def get_form_fields(player):
        return [f'income{i}' for i in range(1, 4)]

    @staticmethod
    def vars_for_template(player: Player):
        fields = [f'income{i}' for i in range(1, 4)]
        labels = [getattr(C, f'income_label{i}') for i in range(1, 4)]
        combined = zip(labels, fields)
        return dict(combined=combined)

#    @staticmethod
#    def before_next_page(player, timeout_happened):
#        player.saw_q3_no_response_error = True
#
#        for i in range(1, 4):
#            if not getattr(player, f'income{i}', 0):
#                setattr(player, f'income{i}', 0)


    @staticmethod
    def before_next_page(player, timeout_happened):
        player.saw_q3_no_response_error = True
        # First try if the bins are empty. If yes, replace with 0
        for i in range(1, 4):
            try:
                getattr(player, 'income' + str(i))
                exec("{0} = {1}".format('player.income' + str(i) + '_by_player', True))
            except TypeError:
                exec("{0} = {1}".format('player.income' + str(i), 0))
                # {0} and {1} are indices to be replaced by the arguments of .format

        incomes = [getattr(player, f'income{i}') for i in range(1, 4)]
        player.income_org_sum = sum_incomes(incomes)
        incomes_by_player = [getattr(player, f'income{i}_by_player') for i in range(1, 4)]
        player.income_org_sum_by_player = sum_incomes(incomes_by_player)

        # Case 1: Beliefs add up to 100
        if player.income_org_sum == 100:
            player.income_org_sum_100 = True
            player.answered_q3 = True

        # Case 2: Beliefs add up to 0 (i.e. participant didn't enter anything)
        # In this case set them to none again to restart the density question
        if player.income_org_sum == 0:
            player.income_org_sum_0 = True
            for i in range(1, 4):
                exec("{0} = {1}".format('player.income' + str(i), None))

        if timeout_happened:
            player.has_timeout = True
            player.session.dropout_treatments.append(player.treatment)

    @staticmethod
    def is_displayed(player: Player):
        return player.stop1 and player.stop2 and player.stop3


class Demo4(Page):
    form_model = "player"
    form_fields = ["spending1", "spending2", "spending3", "spending4", "spending5", "spending6", "spending7",
                   "spending8", "spending9"]

    @staticmethod
    def is_displayed(player: Player):
        return player.stop1 and player.stop2 and player.stop3


class Demo5(Page):
    form_model = "player"
    form_fields = ["major_purchases", "essential_goods", "clothing_and_footwear", "entertainment_recreation",
                   "mobility", "services", "travel_holidays", "housing_costs", "financial_reserves"]

    @staticmethod
    def is_displayed(player: Player):
        return player.stop1 and player.stop2 and player.stop3

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.survey_complete = not timeout_happened

class Demo5b(Page):
    form_model = "player"
    form_fields = ["good_real_estate", "good_car", "good_durable_goods", "good_loans1", "good_loans2"]

    @staticmethod
    def is_displayed(player: Player):
        return player.stop1 and player.stop2 and player.stop3

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.survey_complete = not timeout_happened


class Demo6(Page):
    form_model = "player"
    form_fields = ["unemployment", "rent", "lending", "interest", "inflation", "property"]

    @staticmethod
    def is_displayed(player: Player):
        return player.stop1 and player.stop2 and player.stop3


class Check(Page):
    form_model = 'player'
    form_fields = ['sanity_median', 'sanity_deflation']

    @staticmethod
    def is_displayed(player: Player):
        if player.treatment == 1 or player.treatment == 3:
            if (player.stop1 and player.stop2 and player.stop3) == True :
            #if (player.stop1 and player.stop2 and player.stop3) == True and player.round_number > 1:
                return True
            else:
                return False
        else:
            return True

    @staticmethod
    def error_message(player: Player, values):
        if values['sanity_median'] is None or values['sanity_deflation'] is None:
            return "Please answer the question."


    @staticmethod
    def vars_for_template(player: Player):
        if player.treatment == 2:
            median_check = player.participant.vars.get('median_check')
            median_deflation_check = player.participant.vars.get('median_deflation_check')
            print(f"Treatment 2 - median_check: {median_check}")
            print(f"Treatment 2 - median_deflation_check: {median_deflation_check}")
            return {
                'median_check': round(median_check, 1),
                'median_deflation_check': round(median_deflation_check, 0)
            }
        elif player.treatment == 1:
            if player.round_number > 1:
                final_midpoint = player.in_round(player.round_number - 1).final_midpoint
                print(f"Final midpoint before rounding: {final_midpoint}")
                median_check = round(final_midpoint, 2)  # Specify precision if needed
                print(f"Median check after rounding: {median_check}")
            #THIS IS NEW
            else:
                final_midpoint = player.in_round(player.round_number).final_midpoint
                print(f"Final midpoint before rounding: {final_midpoint}")
                median_check = round(final_midpoint, 2)  # Specify precision if needed
                print(f"Median check after rounding: {median_check}")

            if player.in_round(1).first_min_expectation >= 0:
                median_deflation_check = 0
            else:
                median_deflation_check = calculate_deflation_probability(player)

            return {
                'median_check': round(median_check, 1),
                'median_deflation_check': round(median_deflation_check, 0)
            }
        else:
            return {}


class Final(Page):
    form_model = "player"

    @staticmethod
    def js_vars(player):
        return dict(
            completionlink=
            player.subsession.session.config['completionlink']
        )

    pass

    @staticmethod
    def is_displayed(player: Player):
        if player.treatment == 1 or player.treatment == 3:
            if (player.stop1 and player.stop2 and player.stop3) == True:
                return True
            else:
                return False
        else:
            return True


class Code(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        if player.treatment == 1 or player.treatment == 3:
            if (player.stop1 and player.stop2 and player.stop3) == True:
                return True
            else:
                return False
        else:
            return True


class DemoIntro(Page):

    @staticmethod
    def is_displayed(player: Player):
        if player.treatment == 1:
            if (player.stop1 and player.stop2 and player.stop3) == True:
                return True
            else:
                return False
        else:
            return True


class FinanceIntro(Page):

    @staticmethod
    def is_displayed(player: Player):
        if player.treatment == 1 :
            if (player.stop1 and player.stop2 and player.stop3) == True:
                return True
            else:
                return False
        else:
            return True


page_sequence = [Instructions, Point, info_intro, info_high, info_low, info_control,info_mean, info_uncertainty, InflationsErwartung, Confirmation,
                 InflationsErwartung2, InstructionsP2, Bisection1, Q25Screen,
                 Q25_1, Q75Screen, Q75_1, Bins, Check, Demo7, DemoIntro, Demo1, FinanceIntro, Demo2, Demo3, Demo5, Demo5b, Demo6, Final, Code]


# #page_sequence = [Instructions, Point, info_high, info_low, info_control, InflationsErwartung, Confirmation,
#                  InflationsErwartung3, Bisection1, Q25Screen,
#                  Q25_1, Q75Screen, Q75_1, Bins, Check, Demo7, DemoIntro, Demo1, FinanceIntro, Demo2, Demo3, Demo4,
#                  Demo5, Demo6, Final, Code]