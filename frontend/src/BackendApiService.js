import axios from "axios";
import api_url from "./constants.js";
const API_URL = api_url.DEV; // change when in production to api_url.PROD
export class APIService {
  constructor() {}

  getUser(email) {
    const url = `${API_URL}/api/find/${email}/`;
    const response = axios.get(url);
    return response;
  }

  createUser(email) {
    const url = `${API_URL}/api/register/`;
    const response = axios.post(url, { email });
    return response;
  }

  getCategory(user_id) {
    const url = `${API_URL}/api/GetCategory/${user_id}/`;
    const response = axios.get(url);
    return response;
  }

  getFavThings(category, user) {
    const url = `${API_URL}/api/GetFavThings/${category}/${user}/`;
    const response = axios.get(url);
    return response;
  }

  createCategory(category) {
    const url = `${API_URL}/api/CategoryCreate/`;
    const response = axios.post(url, category);
    return response;
  }

  createThing(thing) {
    const url = `${API_URL}/api/CreateThing/`;
    const response = axios.post(url, thing);
    return response;
  }

  updateThing(thing) {
    const url = `${API_URL}/api/UpdateThing/${thing.id}/`;
    const response = axios.put(url, thing);
    return response;
  }

  deleteThing(thing) {
    const url = `${API_URL}/api/DestroyThing/${thing.id}/`;
    const response = axios.delete(url, thing);
    return response;
  }

  getLogs(user_id) {
    const url = `${API_URL}/api/GetLog/${user_id}/`;
    const response = axios.get(url);
    return response;
  }

  prepareMeta(arr) {
    // function to prepare the metadata and send it back to the backend
    let met_str = "";
    arr.forEach(item => {
      if (item.key != "" && item.value != "") {
        met_str =
          met_str + '{"key":"' + item.key + '", "value":"' + item.value + '"},';
      }
    });
    met_str = met_str.substring(0, met_str.length - 1);
    met_str = "[" + met_str + "]";
    return met_str;
  }
}
