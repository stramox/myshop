import stripe, logging
import traceback

stripe.api_key = 'sk_test_51QXMO5Fhc0MCKfXUH2gB6LDxTa9kgXHP6sWkSGrLzOWENvuIlekTHqc4HMPvDeGN4CB6ZPq6IT0UtHMSDQjufMzj00qGabUHPr'

def example_function(**kwargs):
    try:
        stripe.PaymentIntent.create(**kwargs)
    except stripe.error.CardError as e:
        logging.error("A payment error occurred: {}".format(e.user_message))
    except stripe.error.InvalidRequestError:
        logging.error("An invalid request occurred.")
    except Exception as e:
        logging.error("Another problem occurred, maybe unrelated to Stripe.")
        logging.error(f"Exception: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
    else:
        logging.info("No error.")

example_function(
    amount=2000,
    currency='usd',  # Add currency parameter
    confirm=True,
    payment_method='pm_card_visa',
)
