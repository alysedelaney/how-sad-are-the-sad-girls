import requests 
import base64
import json

# =========================================================================

# Retreives all Track ID's for the artists listed in Compiled_Artist_Info.json. This list of Artist IDs is manually populated here, but could also be written to pull them directly from the JSON file.

#  Spotify does not have an API endpoint to retrieve all of an artist's tracks, so the script first retrieves all albums and singles for each artist, then retrieves the unique track IDs in each of these albums. The resulting data is dropped into a separate JSON file for each artist. This takes a while to run and it's easy to max out the API limits, so adjust list of artist ID's as necessary. Might have to do in several batches.

# =========================================================================
 
# Spotify API Set Up

client_id = "5bae1e05720d486a8bef2310f63cdb05"
client_secret = "8a701744762d47ae801d7bebf730e489"

url = 'https://accounts.spotify.com/api/token'

headers = {}
data = {}

message = f"{client_id}:{client_secret}" 
message_bytes = message.encode('ascii')
base64bytes = base64.b64encode(message_bytes)
base64message = base64bytes.decode('ascii')

headers['Authorization'] = f"Basic {base64message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']

headers = {
    "Authorization": "Bearer " + token
}

base_url = "https://api.spotify.com/v1/"

# --------------------------------------------------------------------------

artist_ids = ['1WVGbBnzZ5WLZ2PfesIHik', '4eArh1v6UwBbKkjdgHCned', '5kdYrM3h2sB1Eid5tDf6Hk', '1CUUXdvZE6UzwQyBUm5YVD', '01y8iBZYk8aeNfPsuTVrAt', '1nEGjL7aMVdNQzsfQPKdGr', '35l9BRT7MXmM8bv2WDQiyB', '03uMw43UVu9MsQCcHVSGjX', '3ir2pF2mkiEWqyPenKTh5e', '3sE8O47mEFWR6pL0rwnAHy', '6t0a2t1BXxTQvAkxReClPm', '6xdRb2GypJ7DqnWAI2mHGn', '1PoFNQQDFXvOYm6Dx8coAa', '5OPhZptrztOU4W75eMEPiX', '2hUYKu1x0UZQXvzCmggvSn', '17mwzDXKn4ra9cuxXaptwp', '2vnB6tuQMaQpORiRdvXF9H', '4E2rKHVDssGJm2SCDOMMJB', '1Uk1GyijF6fSfX4mWq5bfR', '1F2JeQG9fLoC6flF1QTnxS', '66rDbD3tWR3M1uNuIaDAGx', '0SrIPejckovMwhrN3MZFPB', '492I2sQFcHDcsZECYX25dE', '6u6AbTVrbabv27DLcSrF8i', '7bcbShaqKdcyjnmv4Ix8j6', '4Q3A7ukbHFR5xThu9hZDZt', '1wMNhhG8VUhDGZ249MZBtn', '34LdbFt5sVXKTJOzf1iExQ', '4De2r7QdHl1eZwnEnQ1IzE', '73MDShZzdL4vUGMkmXOG6X', '3ETLPQkcEd7z4k3IbZmXMq', '502gYHkFCtLzBIcU4ctPLd', '3rWZHrfrsPBxVy692yAIxF', '3NsSv8HchEwfa7bGkjb4ZC', '7bI1v9NGBBhq8iGfytctni', '3aO4DL5c2uBGD8EUuP7sxi', '1cZQSpDsxgKIX2yW5OR9Ot', '7ovXNdlB2DNSC16TbKgros', '1r1uxoy19fzMxunt3ONAkG', '3diDUq8QMCCtx8a4Jy42aO', '2xCYQunn7ZXK6qOwXWPvcF', '4ClziihVpBeFXNyDH83Lde', '13YVfXddjRIUrubItJjadb', '0avMDS4HyoCEP6RqZJWpY2', '0cz2DZrX5wGn1XUdIPKYYQ', '0EmUT6i9rTu9ZHy1Tl1iuX', '4kIwETcbpuFgRukE8o7Opx', '3SEtmo8E5DJVuGddKYqeiU', '6nB0iY1cjSY1KyhYyuIIKH', '5FkMS3KgG0cjiRm250NFTJ', '2wunbYU5KWrpI7RCRBkwF0', '0fEfMW5bypHZ0A8eLnhwj5', '21TinSsF5ytwsfdyz5VSVS', '4TCXgdDPm10ensLNCVnIYa', '7GlBOeep6PqTfFi59PTUUN', '4blt4zG5qMjWCPymNjDNP5', '1f3ubTd6eyxuy30ddDJQQa', '3l0CmX0FuQjFxr8SK7Vqag', '3lmR0qMiGuoIF9UC54egcG', '6P5NO5hzJbuOqSdyPB7SJM', '0LZac5VicY19QLaIUvIB0G', '58hqTaCiqGrMsNmmm3qL7w', '59aqTTQGnvttJ4BCThaABZ', '2uaMjmR0IE0K3oKTQrNZVQ', '6DdbeAeBlrYj8bNToZv4TY', '1dUrqVHcv2FCXxlIqzIbiG', '7iPH2BRBF9wKa6ljxvdext', '1nwPEi1UZdJtCxBqATpsq3', '4NZvixzsSefsNiIqXn0NDe', '2auiVi8sUZo17dLy1HwrTU', '2MPHBxznH1fj59jbOWY38u', '4xjJOu0MWVWuaDVZOy0Dx2', '0BJeP79i5wKgCqsEEiQ7G0', '5dtPlx7yKOo7KdZGyrfFIq', '0AsThoR4KZSVktALiNcQwW', '5IWCU0V9evBlW4gIeGY4zF', '4GoD5FJCgC0lbzde7ly44M', '5KTykbPcDB4GYS49jcHbWh', '2gI1WfmpFmmgSRojy4Jup2', '5wk7sY8GIg5ihSI09EbWeS', '3Os4q49SgEN0Tv3fxKw3Sp', '4aEuFytRb43SAgjchJDk5e', '4QkSD9TRUnMtI8Fq1jXJJe', '6QCstr3yhEVSZPQyDvvYjK', '06vRrrjT3DBRkhBlXoBdYj', '3Aut8hgiqZSy2qmJluZMU9', '7d0wUlQ0ZXIGFa0YzuBiR6', '2efrqekWSHlvhATD50AG3m', '426VSUSxx9puUYFgp7l7EQ', '42WJFNdxsAgcn9PfjT61Z3', '1EI0B66miJj5Fl408B7E9H', '4faUajx9k93O56nlmpkOuz', '09kXLeOXRyfNQMXRaDO4qA', '6beUvFUlKliUYJdLOXNj9C', '21IgTzfAyrn8DJpEY7F4DM', '1A0WloDoRE88uUwo3wensY', '3vldh5Ceynytj6Iglw4haP', '4AgusFXPk24LCGMMplX34M', '271bbpX3pdCi56ZJA1jQ43', '5dUUxJQg27XaHdKyLYwNg5', '3KlPjpVKfm6vESPL46NDCh', '5cMVRrisBpDkXCVG48epED', '7aO285xSsCbjy0q9zEqXEk', '3u6lPufHw4Oww6D88rv6sB', '4xdEmbimxXyo9wXy9lq3ek', '3Q9WLyqkHw04V6DDtvPWwH', '6zcDLZ62JsbVM1nLrQMzi4', '5poU7FPEYoBlwjzOEWMbX5', '2HysMkOtaumKooHYAlE7wd', '7FxEy78P0oIVEVxdaL9npy', '0i4M8k5IcQpiEH6nBMdfPT', '69761NObDw2KwmmFgZmxzC', '2mirb9SKAm6IUHtPwreoqN', '7zpvy5B9gb5KprNUzNCOEE', '0YJEuTCD642Yp34CoiH0ox', '2AmfMGi3WZMxqFDHissIAe', '0sYlth2PW1zWJMEU2vCukz', '6XoXNsXj8wck0oVUNwxcmF', '2RVvqRBon9NgaGXKfywDSs', '7MoIc5s9KXolCBH1fy9kkw', '41LGTx1fpA69G2ZAJKZntM', '3xz28DkZR6bmPpVh6Rq13t', '2fSBHYgZUSIQPolv5skG5I', '4TZieE5978SbTInJswaay2', '3oqgxdumaZZ5hOt2ykwYTQ', '3Fxg10eJ6YmvUdM2PPB4Zk', '0x4xCoWaOFd3WsKarzaxnW', '4OSArit7O2Jaj4mgf3YN7A', '1GUaQ6GpaxFPKZ0SCSsnwD', '167VlZ0C0ewQbgKexRFcs6', '76oY04bOzECod3aGVTDtzu', '7BsLsPnH5swTyhGZq2qNbN', '1m2tY2Q32cp51czUo7SxyZ', '6ps9u0MZquDDBReh8XuBeY', '1kMPdZQVdUhMDKDWOJM5iK', '5DD5GZd4ElmQTy9NleMvKJ', '0NB5HROxc8dDBXpkIi1v3d', '7lsnwlX6puQ7lcpSEpJbZE', '1KGcdM5KxCVydaHe29QAj9', '5jq01ts8cBQWwVZOpMax6s', '3MNLhvqJkWsO6tcjY9ps62', '2awB7Ol181cocZcLLNBBAh', '574ERIqzZ5yZU9JhIf3Ysf', '6EHS9kZ9PpeXaJ4wZO3FSX', '6f5lOlSFJw9K79gaNnmWAd', '1GmsPCcpKgF9OhlNXjOsbS', '7fnMav7xXJwwjbyWbSjF4C', '2orBKFyc84jo9AZH5jarhI', '1vkWdqcabQ1swciXipkLBj', '3IunaFjvNKj98JW89JYv9u', '3gBjSrNsYzzbeo0nwsL21J', '5RTLRtXjbXI2lSXc6jxlAz', '2mHjhKyKCLh6MZELuCe1Es', '3truyDimkGtu58fxQj9Xv9', '4aej3kKLxSLM0WauTSfZ7k', '1QfEfvB62EEl4upf2ANKkR', '2kQnsbKnIiMahOetwlfcaS', '7qrEXiLLnWkkYHhadZ1Oij', '6IiZemRMna678qNhiRkYI5', '3CGuwWgoCYSO5Z72H5G2Ec', '12fRkVfO2fUsz1QHgDAG3g', '0jzaoSt5gOC04OWBqN78VS', '6VgPyGeGO86DztjK7GCYT3', '5qa31A9HySw3T7MKWI9bGg', '6bEYoIUTLdcs4lZBNVw5L5', '4kpaI92KQcPABQj9qxIopw', '4pdoRs7yHNXakMobf8M9Oz', '3AHFDfqhSqPBecjQDIOIJA', '7AWyYXZ5tIc0xNSfKLD3QX', '6kDXH8d9LugUAsHIozzDAI', '2hR4h1Cao2ueuI7Cx9c7V8', '0eYsDVXAe2mc4F8QrBLHAq', '02zPEtdzUWnPToEVLRiQ7e', '4wXchxfTTggLtzkoUhO86Q', '3GQboECxDT1xqPPWC30p7v', '74CcYmmNeHKe5PrZaISk8e', '7nnTzZ5tZrPx14iDnmjksU', '6mKqFxGMS5TGDZI3XkT5Rt', '3L733apFuBmRr4GEVvhh9x', '1Fr6agZ6iSM5Ynn2k4C8sc', '4pZOG8ump4odtJJA4Cy7S8', '4VqlewwKZJoIcA88PYHUDd', '1hLiboQ98IQWhpKeP9vRFw', '3d7MqowTZa2bC5iy1JXLLt', '5GGJosGMs08YEmKTZJe1fL', '2datC2OML2YxykP6vnDRmg', '2OaHYHb2XcFPvqL3VsyPzU', '2dV0D4uKMB4c8VhYHzt360', '784kOgkd1H6jU4KgPMYHi9', '3ZH4IYVc5qVlKyJoZhGpwy', '4zWJqtFs82kB6LSMY20ggp', '6d6ts87Fxm1EdULf4CaLw4', '5XMyhVhi5ZN2pi0Qwi1zXS', '1wmiQ6ytATiGnJs6uFluKO', '0HthCchcL0kVLHTr113Vk1', '3L9rqEIsNSaOcx2QIstn7v', '5QuBVnBPEzwYvFrgBbwpmU', '2xLEV2jDreAOcpJXFNoXyt', '06W84OT2eFUNVwG85UsxJw', '5e1SaJPn6U7YpOrNTkW1jH', '12zbUHbPHL5DGuJtiUfsip', '5f7gSCzm2HHLDFWrkqZFgm', '3ajf12ub55b51qcS94d9Co', '5NyCIBCeU080ynEj33S4hC', '1LrML89CKJhZjgji63Bvx1', '7D8LuVnlyu91ndcPe70j7S', '1FdUgjmEeGCpmAxXatjiEG', '0t3QQl52F463sxGXb1ckhB', '4aKWmkWAKviFlyvHYPTNQY', '5szilpXHcwOqnyKLqGco5j', '5a3lFI5IJGQbpMTdjrehHl', '2wJ4vsxWd7df7dRU4KcoDe', '5n9jfCRA7AFY1JfYc5ZYK5', '4lPl9gqgox3JDiaJ1yklKh', '3uwAm6vQy7kWPS2bciKWx9', '3qqkHeEhezlIaNj1vFYH2r', '4nxKz1dRYXnsGzN1lUURtG', '22qLnGc8B1btqty6d0Qnlm', '1Kssd2mp7BMKGZUUKncUt6', '07D1Bjaof0NFlU32KXiqUP', '6kDXH8d9LugUAsHIozzDAI', '5ptfrHC6idq4KnsXBk5tup', '5G49Sq5mMzAkGL4ZP6eVPY', '58jk0945bnQBG9xfij6hHw', '294lNTPZfdqyzt8qnxmFiL', '1lVadNivMiSkc2N6irhWdg', '2uYWxilOVlUdk4oV9DvwqK', '1jFVu6Z7wmwywivOeBTSIV', '1Zi1c8sWZTy5rDiN3lAuEj', '4xrDCETyApzUQ6xzcc6QtS', '0Cp8WN4V8Tu4QJQwCN5Md4', '42NjRVKqEGe2DkGvlUd5qM', '4V30Q8ACPdJCcAmAYibfrH', '3P4vW5tzQvmuoNaFQqzy9q', '5ujrA1eZLDHR7yQ6FZa2qA', '7d64ZVOXg02y73HB5UMqkb', '0bsV0sUjnCuCTYOnNHQl3E','1NJUWqbiNAk1BPOyQhb2qe']

# --------------------------------------------------------------------------
# As script is running, if it fails, move the successful ids into "Succeeded" and try again with shorter list
# FAILED: []
# Succeeded:[]
# --------------------------------------------------------------------------

counter = 1
search_total = len(artist_ids)

for artist_id in artist_ids:

    print(f"Retrieving Artist Track IDs: {counter}/{search_total}")
    print(artist_id)

    album_ids = []

    album_url = f"{base_url}artists/{artist_id}/albums"
    params = {
        "include_groups" : "album,single"
    }
    album_res = requests.get(url=album_url, headers=headers, params=params)
    #Print status update on next line if script fails, usually too many requests
    # print(album_res.text)
    album_json = album_res.json()
    
    for album in album_json['items']: 
        if album['id'] not in album_ids:
            album_ids.append(album['id'])
    
    while album_json['next'] is not None:
        album_url = album_json['next']
        album_res = requests.get(url=album_url, headers=headers, params=params)
        album_json = album_res.json()
        for album in album_json['items']: 
            if album['id'] not in album_ids:
                album_ids.append(album['id']) 

    print(f"Found {len(album_ids)} albums. Getting tracks...")

    track_names = []
    track_ids = []

    for album_id in album_ids:
        album_tracks_url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
        params = {
            "limit" : 50,
        }
        album_tracks_res = requests.get(url=album_tracks_url, headers=headers, params=params)
        album_tracks_json = album_tracks_res.json()

        for track in album_tracks_json['items']:
            if track['name'] not in track_names:
                track_names.append(track['name'])
                track_ids.append(track['id'])

    artist_track_dict = {
        "artist_id" : artist_id,
        "tracks" : track_ids
    }

    print(f"{len(track_ids)} tracks found.\n")
    json.dump(artist_track_dict, open(f'data/track_ids_by_artist/{artist_id}.json', 'w'), indent=2)

    counter += 1