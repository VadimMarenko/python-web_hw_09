from models import Authors, Quotes
import connect as connect

# import redis
# from redis_lru import RedisLRU

# client = redis.StrictRedis(host="localhost", port=6379, password=None)
# cache = RedisLRU(client)


# @cache
def name_query(name: str):
    if author := Authors.objects(fullname__istartswith=query[1]).first():
        quotes = Quotes.objects(author=author.id)
    else:
        print("No such author found")
    return quotes


# @cache
def tag_guery(tag: str):
    quotes = list(Quotes.objects(tags__istartswith=query[1]))
    return quotes


# @cache
def tags_query(tags: str):
    if "," in query[1]:
        query_list = query[1].split(",")
    else:
        print("No such tags found")
    quotes = list(Quotes.objects(tags__in=query_list))
    return quotes


if __name__ == "__main__":
    i = True
    while i:
        print("----Search quotes----")
        user_input = input("Input field:value >>>")
        print("---------------------")
        query = user_input.split(":")

        try:
            if query[0] == "exit":
                i = False
                break

            elif query[0] == "name":
                quotes = name_query(query[1])

            elif query[0] == "tag":
                quotes = tag_guery(query[1])

            elif query[0] == "tags":
                quotes = tags_query(query[1])

            else:
                print("No such field exists")

            for quote in quotes:
                print(quote.quote)

        except UnboundLocalError as err:
            print(err)
        except NameError as err:
            print(f"Invalid field value \n {err}")
