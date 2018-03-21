from bot.command import command



@command("lastfm", man = "Obtain most recent played song for a Last.FM user Usage: {leader}{command} <username>")
def lastfm(bot, line):
    import json
    import requests
    from datetime import datetime
    from bot.colors import color

    RECENT_TRACK_URL = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={0}&api_key={1}&format=json"
    TRACK_INFO_URL = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={0}&mbid={1}&username={2}&format=json"

    parts = line.text.split(' ')

    username = parts[0]

    recent_response = requests.get(RECENT_TRACK_URL.format(username, bot.API_KEYS["lastfm"]))
    recent_json = json.loads(recent_response.text)

    try:
        error = recent_json["error"]
        user_exists = False
    except KeyError:
        user_exists = True

    if user_exists:
        last_fm_track_user = recent_json["recenttracks"]["@attr"]["user"]
        try:
            lastfm_track_info = recent_json["recenttracks"]["track"][0]
            track_exists = True
        except IndexError:
            track_exists = False

        if track_exists:
            lastfm_track_mbid = lastfm_track_info["mbid"]
            lastfm_track_song = lastfm_track_info["name"]
            lastfm_track_artist = lastfm_track_info["artist"]["#text"]
            lastfm_track_album = lastfm_track_info["album"]["#text"]
            try:
                lastfm_track_time = lastfm_track_info["@attr"]["nowplaying"]
            except KeyError:
                lastfm_track_time = lastfm_track_info["date"]["#text"]


            info_response = requests.get(TRACK_INFO_URL.format(bot.API_KEYS["lastfm"], lastfm_track_mbid, username))
            info_json = json.loads(info_response.text)

            lastfm_track_playcount = info_json["track"]["userplaycount"]

            msg = "{0}'s last track: \"{1}\" by {2} from the album {3} ({4}) [playcount: {5}]".format(color(last_fm_track_user, 'green'),
                color(lastfm_track_song, 'lightblue'), color(lastfm_track_artist, 'lightblue'),
                color(lastfm_track_album, 'lightblue'), lastfm_track_time, color(lastfm_track_playcount, 'green'))

        else:
            # user exists, track does not
            msg = "{0} has never listened to anything.".format(color(last_fm_track_user, 'green'))
    else:
        # user does not exist
        msg = "User {0} does not exist.".format(color(username, 'green'))

    line.conn.privmsg(line.args[0], msg)