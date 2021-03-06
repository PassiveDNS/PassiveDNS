import axios from "axios";
import config from "./config.json";

export default class PfaApi {
    constructor(jwt) {
        this.service = axios.create({
            baseURL: config.host,
            headers: {
                Authorization: `Bearer ${jwt}`
            }
        });

        this.routes = {
            "dnList": "/dn",
            "dn": "/dn",
            "alert": "/alert",
            "resolution": "/resolution",
            "channels": "/channels",
            "userChannels": "/user/channels",
            "tag": "/tag",
            "tagLinked": "/tag_dn_ip",
            "tagLinkedList": "/tag_dn_ip/list/from",
            "password": "/password"
        };
    }

    getAlertList(filter, filterBy, sortBy, limit) {
        return this.service.get(this.routes.alert, {
            params: {
                days: "1",
                filter: filter,
                filter_by: filterBy,
                sort_by: sortBy,
                limit: limit
            }
        })
            .then(function(d) {
                console.log(d.data.msg);
                return d.data;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    exportAlertList(filter, filterBy, sortBy, limit, exportType) {
        return this.service.get(this.routes.alert, {
            params: {
                days: "1",
                filter: filter,
                filter_by: filterBy,
                sort_by: sortBy,
                limit: limit,
                export: exportType
            }
        })
            .then(function(d) {
                return d.data
            })
    }

    getDnList(owned, followed, filter, filterBy, sortBy, limit) {
        let params = {
            filter: filter,
            filter_by: filterBy,
            sort_by: sortBy,
            limit: limit
        };

        if (owned) {
            params.owned = true
        }

        if (followed) {
            params.followed = true;
        }

        return this.service.get(this.routes.dnList, {
            params: params
        })
            .then(function(d) {
                console.log(d.data.msg);
                return d.data;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    exportDnList(filter, filterBy, sortBy, limit, exportType) {
        return this.service.get(this.routes.dnList, {
            params: {
                filter: filter,
                filter_by: filterBy,
                sort_by: sortBy,
                limit: limit,
                export: exportType
            }
        })
            .then(function(d) {
                return d.data
            })
    }

    getChannelsAvailableList() {
        return this.service.get(this.routes.channels)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.channel_list
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    getChannelLinkedList() {
        return this.service.get(this.routes.userChannels)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.channel_list;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    setupChannel(channelName, contact) {
        return this.service.post(`${this.routes.userChannels}/${channelName}`, {}, {
            params: {
                contact: contact
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

    verifyChannel(channelName, token) {
        return this.service.put(`${this.routes.userChannels}/${channelName}`, {}, {
            params: {
                token: token
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

    testChannel(channelName) {
        return this.service.get(`${this.routes.userChannels}/${channelName}/test`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    removeChannel(channelName) {
        return this.service.delete(`${this.routes.userChannels}/${channelName}`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    createDn(domainName) {
        return this.service.post(`${this.routes.dn}/${domainName}`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false
            })
    }

    getDn(domainName) {
        return this.service.get(`${this.routes.dn}/${domainName}`)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    getDnHistory(domainName) {
        return this.service.get(`${this.routes.resolution}/${domainName}/history`)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.history;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }


    createTag(tag) {
        return this.service.post(`${this.routes.tag}/${tag}`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    getTagList() {
        return this.service.get(this.routes.tag)
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.tag_list;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    getLinkedTagsList(object, type) {
        return this.service.get(this.routes.tagLinkedList, {
            params: {
                object: object,
                type: type
            }
        })
            .then(function(d) {
                console.log(d.data.msg);
                return d.data.tag_link_list;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
            })
    }

    createLinkedTag(object, type, tag) {
        return this.service.post(this.routes.tagLinked, {}, {
            params: {
                object: object,
                type: type,
                tag: tag
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

    deleteLinkedTag(object, type, tag) {
        return this.service.delete(this.routes.tagLinked, {
            params: {
                object: object,
                type: type,
                tag: tag
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

    changePassword(currentPassword, newPassword) {
        return this.service.put(this.routes.password, {
            "current_password": currentPassword,
            "new_password": newPassword
        })
            .then(function(d) {
                console.log(d.data.msg);
                return {b: true, msg: d.data.msg};
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return {b: false, msg: err.response.data.msg};
            })
    }

    follow(dn) {
        return this.service.post(`${this.routes.dn}/${dn}/follow`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    unfollow(dn) {
        return this.service.delete(`${this.routes.dn}/${dn}/follow`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }

    deleteDn(dn) {
        return this.service.delete(`${this.routes.dn}/${dn}`)
            .then(function(d) {
                console.log(d.data.msg);
                return true;
            })
            .catch(function(err) {
                console.log(err.response.data.msg);
                return false;
            })
    }
}