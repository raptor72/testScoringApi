import hashlib
import datetime


def get_score(store, phone, email, birthday=None, gender=None, first_name=None, last_name=None):
    key_parts = [
        first_name or "",
        last_name or "",
        datetime.datetime.strptime(birthday, '%d.%m.%Y').strftime('%Y%m%d') if birthday is not None else "",
    ]
    key = "uid:" + hashlib.md5("".join(key_parts).encode('utf-8')).hexdigest()
    try:
        score = store.cache_get(key) or 0
    except:
        score = 0
    if score:
        return score
    if phone:
        score += 1.5
    if email:
        score += 1.5
    if birthday and gender:
        score += 1.5
    if first_name and last_name:
        score += 0.5
    # cache for 6 minutes
    try:
       store.cache_set(key, score, 60 * 6)
    except:
       pass

    return score


def get_interests(store, cid):
    r = store.get(cid)
    return r




