import pynder
import time, os, sys
import numpy as np

NONSTOP = True
MAXFAILS = 15
DATA_PATH = os.path.join(os.getcwd(), 'data/')
AUTH_FILE = os.path.join(os.getcwd(), 'auth/me.auth')

with open(AUTH_FILE, 'r') as f:
    FB_ID, FB_TOKEN = [l.strip('\n') for l in f.readlines()]


def recAuth(fb_id = FB_ID, fb_token = FB_TOKEN, maxFails = MAXFAILS):

    session = None
    fails = 0

    while session is None and fails < maxFails:
        try:
            session = pynder.Session(facebook_id = fb_id, facebook_token = fb_token)
            print('Login was successful!\n')
        except Exception as e:
            fails += 1
            print(e)
            time.sleep(abs(1 + np.random.randn()))

    return session


def dumpUserInfo(usr, path = DATA_PATH, downloadPictures = True):
    """
    Dump user info into file.
    """

    usrPath = os.path.join(path, usr.id)

    if not os.path.isdir(usrPath):
        os.mkdir(usrPath)
    else:
        print('User already in database... skipping!')
        return

    fields = ('id',
             'share_link',
             'name',
             'age',
             'gender',
             'bio',
             'distance_km',
             'schools',
             'jobs',
             'instagram_username'
             )

    info = {field: getattr(usr, field) for field in fields}
    
    info.update({'birth_date': str(usr.birth_date)})
    info.update({'photos': list(usr.photos)})

    with open(os.path.join(usrPath, 'info.json'), 'w') as f:
        f.write(usr.name)

    if downloadPictures:
        for k, url in enumerate(info['photos']):
            with open(os.path.join(usrPath, 'pic_{}.jpg'.format(k)), 'w') as f:
                try:
                    pic = requests.get(url)
                    f.write(pic.content)
                except Exception as e:
                    print(e.message)


def saveAndLike(session, nonStop = NONSTOP):

    while nonStop:
        likes = session.likes_remaining

        if not likes:
            print('No likes left!')
            wait = session.can_like_in
            nap(wait)
        else:
            print('Swiping!')
            people = session.nearby_users()

            while likes:
                person = people.next()
                print('Saving and liking... {}, {}'.format(usr.name, str(usr.age)))
                dumpUserInfo(person)
                person.like()
                likes = session.likes_remaining
                print('Likes remaining: {}'.format(likes))


def nap(wait):
    then = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+wait))
    print('Waiting until... {}'.format(then))
    time.sleep(wait)


if __name__ == '__main__':
    session = recAuth()
    saveAndLike(session)
