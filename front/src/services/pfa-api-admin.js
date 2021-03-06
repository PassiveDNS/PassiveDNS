import axios from "axios";
import config from "./config.json"

export default class PfaApiAdmin {
    constructor(jwt) {
        this.service = axios.create({
            baseURL: config.host,
            headers: {
                Authorization: `Bearer ${jwt}`
            }
        });

        this.routes = {
            "invite": "/admin/invite",
            "verify": "/admin/verify",
            "request": "/admin/request",
            "requestList": "/admin/request/list",
            "inviteList": "/admin/invite/list",
            "userList": "/admin/users/list",
            "users": "/admin/users",
            "channels": "/admin/channels",
            "scheduler": "/admin/scheduler"
        };
    }

    invite(email) {
        return this.service.post(this.routes.invite, {
            email: email
        })
            .then(function(d) {
                console.log(d.data.msg)
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    verify(email) {
        return this.service.post(this.routes.verify, {
            email: email
        })
            .then(function(d) {
                console.log(d.data.msg)
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    requestList() {
        return this.service.get(this.routes.requestList)
            .then(function(d) {
                return d.data.user_request_list
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    requestDelete(email) {
        return this.service.delete(this.routes.request, {
            data: {
                email: email
            }
        })
            .then(function(d) {
                console.log(d.data.msg)
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    inviteList() {
        return this.service.get(this.routes.inviteList)
            .then(function(d) {
                return d.data.user_pending_list
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    userList() {
        return this.service.get(this.routes.userList)
            .then(function(d) {
                return d.data.user_list
            })
            .catch(function(err) {
                console.log(err.response.msg)
            })
    }

    userDelete(username) {
        return this.service.delete(this.routes.users, {
            params: {
                username: username
            }
        })
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.user
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    channelsList() {
        return this.service.get(this.routes.channels)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.channel_list;
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    channelCreate(name, infos, type) {
        return this.service.post(`${this.routes.channels}/${name}`, infos, {
            params: {
                type: type
            }
        })
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    channelUpdate(name, infos) {
        return this.service.put(`${this.routes.channels}/${name}`, infos)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    channelRemove(name) {
        return this.service.delete(`${this.routes.channels}/${name}`)
            .then(function(d) {
                console.log(d.data.msg);
            })
            .catch(function(err) {
                console.log(err.response.data.msg)
            })
    }

    schedulerCreate(name, password) {
        return this.service.post(`${this.routes.scheduler}/${name}`, {
            password: password
        })
            .then(function(d) {
                console.log(d.data.msg);
                return true
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false
            })
    }

    schedulerUpdate(name, password) {
        return this.service.put(`${this.routes.scheduler}/${name}`, {
            password: password
        })
            .then(function(d) {
                console.log(d.data.msg);
                return true
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false
            })

    }



}