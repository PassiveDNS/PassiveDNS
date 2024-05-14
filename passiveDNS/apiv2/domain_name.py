from time import time

from defang import refang
from fastapi import APIRouter, Depends, HTTPException

from apiv2.auth import get_current_user
from models.domain_name import DomainName
from views.domain_name import dn_list_export
from db.database import ObjectNotFound
from models.domain_name import DomainNameResolutionError, DomainNameFilterNotFound, DomainNameSortNotFound,\
    DOMAIN_NAME_COLLECTION
from models.ip_address import IPAddress, IP_ADDRESS_COLLECTION
from models.resolution import Resolution
from models.tag_dn_ip import TagDnIP
from models.users_dn import UserDn
from models.user import User

domain_name_router = APIRouter()


@domain_name_router.get("/dn")
def manage_domain_name_list(
    filter: str, 
    filter_by: str, 
    sort_by: str, 
    limit: str, 
    export: str, 
    owned: str, 
    followed: str, 
    user: User=Depends(get_current_user)
):
    try:
        username = user.username

        input_filter = filter
        input_filter_by = filter_by
        limit_str = limit

        owned_filter = owned
        followed_filter = followed

        if not limit_str.isdigit():
            raise HTTPException(status_code=400, detail='invalid limit')

        limit_int = int(limit_str)

        t1 = time()
        dn_list = DomainName.list(
            username, input_filter, input_filter_by,
            owned_filter, followed_filter,
            sort_by, limit_int
        )
        t2 = time()
        transaction_time = round(t2 - t1, 2)

        if export is not None and export != '':
            # export file data
            return dn_list_export(dn_list, export)
        else:
            # export json data
            return {
                "msg": "domain name list retrieved",
                "stats": {
                    "transaction_time": transaction_time,
                    "count": len(dn_list),
                },
                "dn_list": dn_list
            }

    except DomainNameFilterNotFound:
        raise HTTPException(status_code=400, detail="invalid filter field")

    except DomainNameSortNotFound:
        raise HTTPException(status_code=400, detail="invalid sort field")

@domain_name_router.post("/dn/{domain_name}")
def create_domain_name(domain_name, user: User=Depends(get_current_user)):
    domain_name = refang(domain_name)
    try:
        if DomainName.exists(domain_name):
            raise HTTPException(status_code=500, detail=f"domain name {domain_name} already exists")

        dn = DomainName.new(domain_name)
        dn.insert()

        ip_address = dn.resolve()

        # in case resolutions went fine
        if ip_address is not None:
            if not IPAddress.exists(ip_address):
                ip = IPAddress.new(ip_address)
                ip.insert()

            resolution = Resolution.new(domain_name, ip_address)
            resolution.insert()

        # create user link
        username = user.username
        user_dn = UserDn.new(username, dn.domain_name, True)
        user_dn.insert()

        return {
            "msg": "domain name created",
            "dn": dn.json()
        }

    except HTTPException as dre:
        raise HTTPException(status_code=500, detail=str(dre))

@domain_name_router.get("/dn/{domain_name}")
def get(domain_name, user: User=Depends(get_current_user)):
    domain_name = refang(domain_name)

    dn = None
    dn_tags = []
    owned = False
    followed = False

    username = user.username
    try:
        dn = DomainName.get(domain_name)
        dn_tags = TagDnIP.list_tags_from_object(
            dn.domain_name, DOMAIN_NAME_COLLECTION)

        if not UserDn.exists(username, domain_name):
            owned = False
            followed = False
        else:
            user_dn = UserDn.get(username, domain_name)
            owned = user_dn.owned
            followed = True

        resolution = Resolution.get_current_from_domain(dn.domain_name)

        ip = IPAddress.get(resolution.ip_address)
        ip_tags = TagDnIP.list_tags_from_object(ip.address, IP_ADDRESS_COLLECTION)

        return {
            "msg": "domain name retrieved",
            "dn": dn.json(),
            "dn_tags": [t.tag for t in dn_tags],
            "ip": ip,
            "ip_tags": [t.tag for t in ip_tags],
            "owned": owned, "followed": followed
        }

    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=str(o))

    except DomainNameResolutionError:
        return {
            "msg": "domain name retrieved",
            "dn": dn.json(),
            "dn_tags": [t.tag for t in dn_tags],
            "ip": None,
            "ip_tags": [],
            "owned": owned, "followed": followed
        }

@domain_name_router.put("/dn/{domain_name}")
def put(domain_name):
    domain_name = refang(domain_name)

    try:
        dn = DomainName.get(domain_name)
        ip_address = dn.resolve()
        if ip_address is None:
            raise HTTPException(status_code=404, detail="resolution not found")

        if not IPAddress.exists(ip_address):
            # the DN resolves a new address
            ip = IPAddress.new(ip_address)
            ip.insert()

        if not Resolution.exists(domain_name, ip_address):
            # ip change detected
            resolution = Resolution.new(domain_name, ip_address)
            resolution.insert()

        else:
            resolution = Resolution.get(domain_name, ip_address)
            resolution.update()

        dn.update()
        return {
            "msg": "domain name modified",
            "dn": dn.json()
        }

    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=str(o))

    except DomainNameResolutionError as dre:
        raise HTTPException(status_code=500, detail=str(dre))

@domain_name_router.delete("/dn/{domain_name}")
def delete(domain_name, user: User=Depends(get_current_user)):
    domain_name = refang(domain_name)

    try:
        username = user.username
        if not UserDn.exists(username, domain_name):
            raise HTTPException(status_code=403, detail="no ownership found")

        # remove ownership
        user_dn = UserDn.get(username, domain_name)
        if not user_dn.owned:
            raise HTTPException(status_code=403, detail="you do not own this domain")

        user_dn.delete()

        # remove tags
        dn_linked_tags = TagDnIP.list_tags_from_object(
            domain_name, DOMAIN_NAME_COLLECTION)
        for t in dn_linked_tags:
            t.delete()

        # remove resolution / IP
        resolution_list = Resolution.list_from_domain(domain_name)
        for r in resolution_list:
            r.delete()

            ip_address = r.ip_address
            res_ip_list = Resolution.list_from_ip(ip_address)
            if len(res_ip_list) == 0:
                ip_linked_tags = TagDnIP.list_tags_from_object(
                    ip_address, IP_ADDRESS_COLLECTION)
                for t in ip_linked_tags:
                    t.delete()

                ip = IPAddress.get(ip_address)
                ip.delete()

        dn = DomainName.get(domain_name)
        dn.delete()

        return {
            "msg": "domain name deleted",
            "dn": dn.json()
        }
    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=str(o))


@domain_name_router.post("/dn/{domain_name}/follow")
def manage_follow(domain_name, user: User=Depends(get_current_user)):
    domain_name = refang(domain_name)
    username = user.username

    if UserDn.exists(username, domain_name):
        raise HTTPException(status_code=500, detail="you are already following this DN")

    user_dn = UserDn.new(username, domain_name, False)
    user_dn.insert()
    return {
        "msg":"DN added to your follows"
    }


@domain_name_router.delete("/dn/{domain_name}/follow")
def remowe_follow(domain_name, user: User=Depends(get_current_user)):
    domain_name = refang(domain_name)
    username = user.username

    if not UserDn.exists(username, domain_name):
        raise HTTPException(status_code=404, detail="you are not following this DN")

    user_dn = UserDn.get(username, domain_name)
    user_dn.delete()
    return {
        "msg":"DN removed from your follows"
    }
