<template>
    <div class="mb-4">
        <h3>Available channels</h3>
        <div class="row" v-if="channelsList.length > 0">
            <div class="col-" v-for="c in channelsList" :key="c._key">
                <div class="card m-1" style="width: 20rem;">
                    <div class="card-header">
                        <img v-if="c.type === channelTypeEmail" class="mr-2 light"
                             src="../../../assets/icons/icons8-mail-48.png" alt="mail">
                        <img v-else-if="c.type === channelTypeTelegram" class="mr-2 light"
                             src="../../../assets/icons/icons8-telegram-app-48.png" alt="telegram">
                        <img v-else-if="c.type === channelTypeDiscord" class="mr-2 light"
                             src="../../../assets/icons/icons8-discord-48.png" alt="discord">
                        <span style="font-size: 24px" class="card-title">{{c._key}}</span>
                    </div>
                    <div class="card-body">
                        <span class="card-link">
                            <button @click="setup(c)" class="btn btn-primary">
                                <img src="../../../assets/icons/icons8-settings-24.png" alt="setup">
                                Setup
                            </button>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ChannelsAvailableList",
        props: {
            channelsList: Array,
            channelTypeEmail: String,
            channelTypeTelegram: String,
            channelTypeDiscord: String,
        },
        methods: {
            setup(channel) {
                this.$emit('setup', channel)
            }
        }
    }
</script>

<style scoped>

</style>