class WowoApi {

  #urlPrefix = "https://app.woyouzhijia.cn/app";

  async #getResponse(url) {
    const response = await fetch(url, {
      cache: 'force-cache',
      referrerPolicy: 'no-referrer',
    });
    const data = await response.json();
    if (data["errno"]) {
      throw new Error(data["errmsg"]);
    }
    return data["data"]
  }

  async getWowoList(lat, lng, range = 20) {
    const qp = new URLSearchParams({
      latitude: lat,
      longitude: lng,
      limit: 1000,
      page: 1,
      range: range,
      type: true,
    });
    const url = `${this.#urlPrefix}/community/site/search/findBasicWoWo?${qp}`;
    return await this.#getResponse(url);
  }

  async getWowo(siteId) {
    const url = `${this.#urlPrefix}/community/site/get?siteId=${siteId}`;
    return await this.#getResponse(url);
  }
}

export default new WowoApi();
