class AmapApi {
  // TODO: Don't store key in code.
  key = import.meta.env.VITE_AMAP_KEY;

  async getGeoCode(address) {
    const qp = new URLSearchParams({
      address: address,
      key: this.key,
    });
    const response = await fetch(
      `https://restapi.amap.com/v3/geocode/geo?${qp}`
    );
    const data = await response.json();
    if (
      data["status"] == "1" &&
      data["geocodes"] &&
      data["geocodes"].length > 0
    ) {
      return data["geocodes"][0];
    }
    throw new Error(data["info"]);
  }
}

export default new AmapApi();
