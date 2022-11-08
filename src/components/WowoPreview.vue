<script>
import wowoApi from '../wowoApi.js';

export default {
    data() {
        return {
            loading: true,
            images: [],
            address: [],
            description: "",
            icons: [],
            style: "",
            favorites: 0,
            rewards: 0,
            shares: 0,
            rating: 0,
        }
    },
    props: {
        siteId: Number,
    },
    async mounted() {
        const wowo = await wowoApi.getWowo(this.siteId);
        this.loading = false;

        this.images = wowo.subSite.imageList;
        this.address = wowo.subSite.address;
        this.description = wowo.subSite.description;
        this.style = wowo.subSite.style;

        const iconList = await wowoApi.getWowoIcons();
        this.icons = iconList.filter(icon => icon.id == 24 || icon.id == 25).map(icon => wowo.subSite.iconList.includes(icon.id) ? icon["selectedIcon"] : icon["unselectedIcon"]);

        this.favorites = wowo.countCollect;
        this.rewards = wowo.countReward;
        this.shares = wowo.countShare;
        this.rating = wowo.averageScore;
    }
};
</script>

<template>
    <p v-if="loading">加载中……</p>
    <div class="container" v-if="!loading">
        <div class="mainPreview">
            <div>
                <img class="pic" :src="images[0]" />
                <div class="style">{{ style }}</div>
            </div>
            <div>
                <div class="description">{{ description }}</div>
                <div class="addressLine">
                    <span class="pin">📍</span>
                    <span>{{ address }}</span>
                </div>
                <div>
                    <img class="icon" v-for="icon in icons" :src="icon" />
                </div>

            </div>
        </div>
        <div class="stats">
            <span>❤️ {{ favorites }}</span>
            <span>🪙 {{ rewards }}</span>
            <span>↗️ {{ shares }}</span>
            <span>⭐️ {{ rating }}</span>
        </div>
    </div>
</template>

<style>
.container {
    margin: 10px;

    border-style: solid;
    border-color: lightgray;
    border-width: medium;
    border-radius: 5px;

    background-color: lavender;
}

.mainPreview {
    display: flex;
}

.pic {
    padding: 10px;
    object-fit: cover;
    width: 100px;
    height: 100px;
}

.icon {
    width: 50px;
    height: 50px;
}

.description {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    /* number of lines to show */
    -webkit-line-clamp: 4;
    line-clamp: 4;
    -webkit-box-orient: vertical;

    font-size: 0.8em;
    margin-top: 10px;
}

.style {
    text-align: center;
}

.pin {
    margin-right: 10px;
}

.addressLine {
    margin: 10px 0;
    font-size: 0.8em;
}

.stats * {
    margin-right: 10px;
}
</style>
