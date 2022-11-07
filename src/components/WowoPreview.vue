<script>
import wowoApi from '../wowoApi.js';

export default {
    data() {
        return {
            loading: true,
            name: "",
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

        this.name = wowo.subSite.name;
        this.images = wowo.subSite.imageList;
        this.address = wowo.subSite.address;
        this.description = wowo.subSite.description;
        this.style = wowo.subSite.style;

        const iconList = await wowoApi.getWowoIcons();
        this.icons = iconList.map(icon => wowo.subSite.iconList.includes(icon.id) ? icon["selectedIcon"] : icon["unselectedIcon"]);

        this.favorites = wowo.countCollect;
        this.rewards = wowo.countReward;
        this.shares = wowo.countShare;
        this.rating = wowo.averageScore;
    }
};
</script>

<template>
    <div>
        <p v-if="loading">加载中……</p>
        <template v-if="!loading">
            <p>{{ name }}</p>
            <img class="pic" :src="images[0]" />
            <p>{{ description }}</p>
            <p>{{ address }}</p>
            <p>{{ style }}</p>
            <img class="icon" v-for="icon in icons" :src="icon" />
            <p>
                <span>收藏数: {{ favorites }}</span>
                <span>奖励数: {{ rewards }}</span>
                <span>分享数: {{ shares }}</span>
                <span>评分: {{ rating }}</span>
            </p>
        </template>
    </div>
</template>

<style>
.pic {
    width: 200px;
}

.icon {
    width: 50px;
}
</style>
