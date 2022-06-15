# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

import json
import requests
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        url = "https://api.weather.com/v2/pws/observations/current?stationId=KMNFRAZE8&format=json&units=e&apiKey=57817431c62d4f13817431c62def1391"

        content = requests.get(url)
        wx_data = content.json()
        observations = wx_data['observations']
        observations = observations[0]
        imperial = observations['imperial']


        temp = imperial['temp']
        heatIndex = imperial['heatIndex']
        dewpt = imperial['dewpt']
        windChill = imperial['windChill']
        windSpeed = imperial['windSpeed']
        windGust = imperial['windGust']
        pressure = imperial['pressure']
        stationID = observations['stationID']
        neighborhood = observations['neighborhood']
        solarRadiation = observations['solarRadiation']
        winddir = observations['winddir']
        humidity = observations['humidity']
        
        if windSpeed != windGust:
            wind = (str(windSpeed) + " mile per hour winds and gusts up to " + str(windGust) + " miles per hour.")
        
        elif windSpeed == 0 or windGust == 0:
            wind = ("calm winds.")
        
        elif windSpeed == windGust:
            wind = (str(windSpeed) + " mile per hour winds.")


        weather = ("It is currently " + str(temp) + " degrees outside, with " + wind + " Say detailed report to hear more.")

        
        
        speak_output = ("Welcome to Tovin's Rose Lake Weather skill. " + weather)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



class DetailedReportIntentHandler(AbstractRequestHandler):
    """Handler for Detailed Rose Lake Weather Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DetailedReportIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        url = "https://api.weather.com/v2/pws/observations/current?stationId=KMNFRAZE8&format=json&units=e&apiKey=57817431c62d4f13817431c62def1391"

        content = requests.get(url)
        wx_data = content.json()
        observations = wx_data['observations']
        observations = observations[0]
        imperial = observations['imperial']


        temp = imperial['temp']
        heatIndex = imperial['heatIndex']
        dewpt = imperial['dewpt']
        windChill = imperial['windChill']
        windSpeed = imperial['windSpeed']
        windGust = imperial['windGust']
        pressure = imperial['pressure']
        stationID = observations['stationID']
        neighborhood = observations['neighborhood']
        solarRadiation = observations['solarRadiation']
        winddir = observations['winddir']
        humidity = observations['humidity']
        precipRate = imperial['precipRate']
        precipTotal = imperial['precipTotal']


        if windSpeed != windGust:
            wind = ("The winds are from " + str(winddir) + " degrees at " + str(windSpeed) + " miles per hour, gusting up to " + str(windGust) + " miles per hour with a wind chill of " + str(windChill) + " degrees. ")
        elif windSpeed == 0:
            wind = ("The winds are currently calm with no wind chill. ")
        else:
            wind = ("The winds are from " + str(winddir) + " degrees at " + str(windSpeed) + " miles per hour with a wind chill of " + str(windChill) + " degrees. ")
            
        if solarRadiation == 0:
            solarRadiation = int(solarRadiation)
            
        if precipRate == 0:
            precipRate = int(precipRate)
            
        if precipTotal == 0:
            precipTotal = int(precipTotal)
            
        if precipRate == precipTotal:
            rain = (" Solar radiation is " + str(solarRadiation) + " watts per meters squared with " + str(precipTotal) + " inches of rain recently. ")
        else:
            rain = (" Solar radiation is " + str(solarRadiation) + " watts per meters squared with " + str(precipRate) + " inches of rain in the last hour, and " + str(precipTotal) + " inches in the last 24 hours. ")
        
        timedate = observations["obsTimeLocal"]

        time = timedate.split(' ')

        time = time[1]

        time = time.split(':')

        hour = time[0]
        minute = time[1]
        second = time[2]

        if int(hour) >= 13:
            hour = int(hour) - 12
            time = ("This data was fetched at " + str(hour) + " " + str(minute) + " PM.  Thank you for using Tovin's Weather Skill for Alexa.")
        else:
            time = ("This data was fetched at " + str(hour) + " " + str(minute) + " AM.  Thank you for using Tovin's Weather Skill for Alexa.")
        
        temperature = (" The temperature outside is " + str(temp) + " degrees, with " + str(humidity) + "% humidity and a dewpoint of " + str(dewpt) + " degrees. ")
        
        mmHg = (" The atmospheric pressure is " + str(pressure) + " inches of mercury. ")
        
        weather = wind + temperature + rain + mmHg + time
        
        speak_output = weather

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Thank you for using Tovin's Rose Lake Weather skill. You can say detailed report to hear the full weather report!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can ask for the detailed weather report. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(DetailedReportIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()