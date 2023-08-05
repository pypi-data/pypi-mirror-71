import vrcpy.objects as o
import vrcpy.types as types

## Avatar

class Avatar(o.Avatar):
    async def author(self):
        resp = await self.client.api.call("/users/"+self.authorId)
        self.client._raise_for_status(resp)
        return User(self.client, resp["data"])

## User

class LimitedUser(o.LimitedUser):
    async def fetch_full(self):
        resp = await self.client.api.call("/users/"+self.id)
        self.client._raise_for_status(resp)

        return User(self.client, resp["data"])

    async def public_avatars(self):
        '''
        Returns array of Avatar objects owned by user object
        '''

        resp = await self.client.api.call("/avatars",
            params={"userId": self.id})
        self.client._raise_for_status(resp)

        avatars = []
        for avatar in resp["data"]:
            avatars.append(Avatar(self.client, avatar))

        return avatars

    async def unfriend(self):
        '''
        Returns void
        '''

        resp = await self.client.api.call("/auth/user/friends/"+self.id, "DELETE")
        self.client._raise_for_status(resp)

    async def friend(self):
        '''
        Returns Notification object
        '''

        resp = await self.client.api.call("/user/"+self.id+"/friendRequest", "POST")
        self.client._raise_for_status(resp)

        return o.Notification(self.client, resp["data"])

class User(o.User, LimitedUser):
    async def fetch_full(self):
        user = await LimitedUser.fetch_full(self)
        return user

    async def public_avatars(self):
        avatars = await LimitedUser.public_avatars(self)
        return avatars

    async def unfriend(self):
        await LimitedUser.unfriend()

    async def friend(self):
        notif = await LimitedUser.friend()
        return notif

class CurrentUser(o.CurrentUser, User):
    obj = "CurrentUser"

    async def fetch_full(self):
        user = await LimitedUser.fetch_full(self)
        return user

    async def public_avatars(self):
        avatars = await LimitedUser.public_avatars(self)
        return avatars

    async def unfriend(self):
        raise AttributeError("'CurrentUser' object has no attribute 'unfriend'")

    async def friend(self):
        raise AttributeError("'CurrentUser' object has no attribute 'friend'")

    async def update_info(self, email=None, status=None,\
        statusDescription=None, bio=None, bioLinks=None):

        params = {"email": email, "status": status, "statusDescription": statusDescription,\
            "bio": bio, "bioLinks": bioLinks}

        for p in params:
            if params[p] == None: params[p] = getattr(self, p)

        resp = await self.client.api.call("/users/"+self.id, "PUT", params=params)
        self.client._raise_for_status(resp)

        self.client.me = CurrentUser(self.client, resp["data"])
        return self.client.me

    async def avatars(self, releaseStatus=types.ReleaseStatus.All):
        '''
        Returns array of Avatar objects owned by the current user

            releaseStatus, string
            One of types type.ReleaseStatus
        '''

        resp = await self.client.api.call("/avatars",
            params={"releaseStatus": releaseStatus, "user": "me"})
        self.client._raise_for_status(resp)

        avatars = []
        for avatar in resp["data"]:
            if avatar["authorId"] == self.id:
                avatars.append(Avatar(self.client, avatar))

        return avatars

    async def __cinit__(self):
        if hasattr(self, "currentAvatar"):
            self.currentAvatar = await self.client.fetch_avatar(self.currentAvatar)

        self.onlineFriends = await self.client.fetch_friends()
        self.offlineFriends = await self.client.fetch_friends(offline=True)
        self.friends = self.onlineFriends + self.offlineFriends

        if hasattr(self, "activeFriends"):
            naf = []
            for fid in self.activeFriends:
                for f in self.friends:
                    if f.id == fid:
                        naf.append(f)
                        break

            self.activeFriends = naf

        if hasattr(self, "homeLocation"):
            self.homeLocation = await self.client.fetch_world(self.homeLocation)

        # Wait for all cacheTasks
        await self.homeLocation.cacheTask

        self.client.cacheFull = True

## World

class LimitedWorld(o.LimitedWorld):
    async def author(self):
        resp = await self.client.api.call("/users/"+self.authorId)
        self.client._raise_for_status(resp)
        return User(self.client, resp["data"])

class World(o.World, LimitedWorld):
    async def author(self):
        resp = await super(LimitedWorld, self).author()
        return resp

    async def fetch_instance(self, id):
        '''
        Returns Instance object

            id, str
            InstanceID of instance
        '''

        resp = await self.client.api.call("/instances/"+self.id+":"+id)
        self.client._raise_for_status(resp)

        return Instance(self.client, resp["data"])

    async def __cinit__(self):
        instances = []
        for instance in self.instances:
            instances.append(await self.fetch_instance(instance[0]))

        self.instances = instances

class Instance(o.Instance):
    async def world(self):
        resp = await self.client.api.call("/worlds/"+self.worldId)
        self.client._raise_for_status(resp)
        return World(resp["data"])
