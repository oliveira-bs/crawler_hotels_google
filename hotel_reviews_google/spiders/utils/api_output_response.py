import itertools
import json
import logging
import re

import requests


def output_reviews_api(response_json: list, **kwargs):
    index = 0
    word_index = 0
    start_index = index
    list_reviews = []

    for index in itertools.count(start=start_index, step=1):
        try:
            properties_review = response_json[2][index]

            try:
                id = properties_review[0][1][4][1][3]
            except TypeError:
                id = None

            try:
                review_age = properties_review[0][1][6]
                review_age = review_age.split("atrás")[0]
            except TypeError:
                review_age = None

            try:
                score = properties_review[0][2][0][0]
            except TypeError:
                score = None

            try:
                language = properties_review[0][2][1][1]
            except (TypeError, IndexError):
                language = None

            try:
                positive_review = properties_review[0][2][15][0][0]
            except (TypeError, IndexError):
                positive_review = None

            try:
                negative_review = properties_review[0][2][1][2]
            except (TypeError, IndexError):
                negative_review = None

            try:
                list_rating = properties_review[0][2][6]

            except (TypeError, IndexError):
                list_rating = None

            if list_rating is not None:
                for rating in list_rating:
                    leader_element = rating[0][0]

                    if "TRIP_TYPE" in leader_element:
                        try:
                            trip_type = rating[2][0][0][1]
                            break
                        except (TypeError, IndexError):
                            trip_type = None
                    else:
                        trip_type = None

                for rating in list_rating:
                    leader_element = rating[0][0]

                    if "GROUP_TYPE" in leader_element:
                        try:
                            group_trip = rating[2][0][0][1]
                            break
                        except (TypeError, IndexError):
                            group_trip = None
                    else:
                        group_trip = None

                for rating in list_rating:
                    leader_element = rating[0][0]

                    if "ASPECT_ROOMS" in leader_element:
                        try:
                            room_rating = rating[11][0]
                            break
                        except (TypeError, IndexError):
                            room_rating = None
                    else:
                        room_rating = None

                for rating in list_rating:
                    leader_element = rating[0][0]
                    if "ASPECT_SERVICE" in leader_element:
                        try:
                            service_rating = rating[11][0]
                            break
                        except (TypeError, IndexError):
                            service_rating = None
                    else:
                        service_rating = None

                for rating in list_rating:
                    leader_element = rating[0][0]
                    if "ASPECT_LOCATION" in leader_element:
                        try:
                            location_rating = rating[11][0]
                            break
                        except (TypeError, IndexError):
                            location_rating = None
                    else:
                        location_rating = None

                for rating in list_rating:
                    leader_element = rating[0][0]
                    if "VIBE" in leader_element:
                        list_highlights = []

                        for word_index in itertools.count(start=start_index,
                                                          step=1):
                            try:
                                highlights_hotel = rating[3][0][word_index][1]
                                list_highlights.append(
                                    highlights_hotel)
                            except IndexError:
                                break
                    else:
                        list_highlights = [None]

            else:
                trip_type = None
                group_trip = None
                room_rating = None
                service_rating = None
                location_rating = None
                list_highlights = [None]

            try:
                guest_reviews = properties_review[0][1][4][0][1]
            except (TypeError, IndexError) as e:
                logging.warning(f"Error guest_reviews\n{e}")
                guest_reviews = None
            try:
                guest_photos = properties_review[0][1][4][0][2]
            except (TypeError, IndexError) as e:
                logging.warning(f"Error guest_photos\n{e}")
                guest_photos = None

            try:
                source = properties_review[0][1][13][0]
            except (TypeError, IndexError) as e:
                logging.warning(f"Error source\n{e}")
                source = None

            output_partial_reviews = {
                "id": id,
                "review_age": review_age,
                "score": score,
                "language": language,
                "type_trip": trip_type,
                "group_trip": group_trip,
                "room_rating": room_rating,
                "service_rating": service_rating,
                "location_rating": location_rating,
                "guest_reviews": guest_reviews,
                "guest_photos": guest_photos,
                "highlights_hotel": list_highlights,
                "source": source,
                "positive_review": positive_review,
                "negative_review": negative_review,

            }

            list_reviews.append(output_partial_reviews)

        except IndexError:
            break

    return list_reviews


def output_hotels_api(response_json: list, **kwargs):
    highlights = []

    try:
        full_address = response_json[6][2]
        if len(full_address) == 3:
            address = full_address[0]
        elif len(full_address) == 4:
            address = full_address[1]
    except TypeError:
        address = None

    try:
        full_address = response_json[6][2]
        if len(full_address) == 3:
            city_province = full_address[1]
        elif len(full_address) == 4:
            city_province = full_address[2]
    except TypeError:
        city_province = None

    try:
        full_address = response_json[6][2]
        if len(full_address) == 3:
            zip_code = full_address[2]
        elif len(full_address) == 4:
            zip_code = full_address[3]
    except TypeError:
        zip_code = None

    try:
        full_id = response_json[6][10]
        split_id = full_id.split(':')
        id = "".join(split_id)
    except TypeError:
        id = None

    try:
        type = response_json[6][13]
    except TypeError:
        type = [None]

    try:
        coordinates = response_json[4][0]
        longitude = coordinates[1]
        latitude = coordinates[2]
    except TypeError:
        longitude = None
        latitude = None

    try:
        link = response_json[6][27]
    except TypeError:
        link = None

    try:
        phone = response_json[6][178][0][1][1][0]
    except TypeError:
        phone = None

    try:
        name = response_json[6][11]
    except TypeError:
        name = None

    try:
        all_highlights = response_json[6][64][2]
        for nth_highlight in all_highlights:
            if nth_highlight[3] == 1:
                highlight = nth_highlight[2]
                highlights.append(highlight)
    except TypeError:
        highlight = [None]

    dict_hotel_output = {
        "id": id,
        "name": name,
        "address": address,
        "city_province": city_province,
        "zip_code": zip_code,
        "type": type,
        "longitude": longitude,
        "latitude": latitude,
        "phone": phone,
        "link": link,
    }

    return {"dict_hotel_output": dict_hotel_output,
            "id": id, "name": name}


def output_hotel_prices(response_json: list, **kwargs):
    output_prices = []
    vars_output_hotel = kwargs.get('vars_output_hotel')
    for index in itertools.count(start=0, step=1):
        try:
            properties_price = response_json[6][35][44][index]

            try:
                service_name = properties_price[0]
            except TypeError:
                service_name = None

            try:
                regex = '[^("\\xa0")][(\\d)]+'
                dirty_price = properties_price[1]
                match_price = re.findall(regex, dirty_price)
                price = match_price[0]
            except TypeError:
                price = None

            try:
                service_id = properties_price[5][3]
            except TypeError:
                service_id = None

            output_price = {
                'service_name': service_name,
                'price': price,
                'service_id': service_id,
            }

            output_price.update(vars_output_hotel)

            order_keys = ['hotel_id', 'hotel_name', 'service_name', 'price',
                          'service_id']
            output_price = {key: output_price[key] for key in order_keys}

            output_prices.append(output_price)

        except IndexError:
            break

        except TypeError:
            service_name = None
            price = None
            service_id = None

            output_price = {
                'service_name': service_name,
                'price': price,
                'service_id': service_id,
            }

            break

    return output_prices


def parse_api_hotel(response, **kwargs):
    global dict_hotel_output
    global vars_output_hotel
    global hotel_prices

    content = response.headers.get('content-type')
    urls_hotels_api = kwargs.get('urls_hotels_api')

    if 'place?authuser' in response.url and 'json' in content \
            and response.url not in urls_hotels_api:

        urls_hotels_api.append(response.url)
        try:
            headers = response.request.headers
            payload = {}

            response_json = requests.request("GET", response.url,
                                             headers=headers,
                                             data=payload)
            response_json = json.loads(response_json.text.split(")]}'")
                                       [-1])

            hotel_output = output_hotels_api(
                response_json=response_json,
                urls_hotels_api=urls_hotels_api)

            vars_output_hotel = {
                "hotel_id": hotel_output.get('id'),
                "hotel_name": hotel_output.get('name')
            }

            hotel_prices = output_hotel_prices(
                response_json=response_json,
                vars_output_hotel=vars_output_hotel)

            dict_hotel_output = hotel_output.get(
                'dict_hotel_output')

            return vars_output_hotel, dict_hotel_output, hotel_prices

        except ConnectionError as e:
            logging.warning(f"Error connection API: \n{e}")


def parse_api_review(response, **kwargs):
    global output_reviews

    content = response.headers.get('content-type')
    urls_reviews_api = kwargs.get('urls_reviews_api')

    if 'listugcposts' in response.url and 'json' in content \
            and response.url not in urls_reviews_api:
        urls_reviews_api.append(response.url)

        try:
            headers = response.request.headers
            payload = {}
            response_json = requests.request("GET", response.url,
                                             headers=headers,
                                             data=payload)

            response_json = json.loads(response_json.text.split(")]}'")
                                       [-1])

            output_reviews = output_reviews_api(
                response_json=response_json,
                urls_reviews_api=urls_reviews_api)

            return output_reviews

        except ConnectionError as e:
            logging.warning(f"Error connection API: \n{e}")


def response_parse_api_hotel():
    try:
        from .api_output_response import (dict_hotel_output, hotel_prices,
                                          vars_output_hotel)
        return dict_hotel_output, vars_output_hotel, hotel_prices
    except Exception as e:
        logging.error(e)
        return None


def response_parse_api_reviews():
    try:
        from .api_output_response import output_reviews
        return output_reviews
    except Exception as e:
        logging.error(e)
