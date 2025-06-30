import { createApp } from "vue";
import App from "./App.vue";
import './style.css'
import router from "./router";
import resourceManager from "../../../doppio/libs/resourceManager";
import call from "../../../doppio/libs/controllers/call";
import socket from "../../../doppio/libs/controllers/socket";

// Khởi tạo app
const app = createApp(App);

// Plugins
app.use(router);
app.use(resourceManager);

// Global Properties, inject dùng được trong components
app.provide("$call", call);
app.provide("$socket", socket);

// Mount app
app.mount("#app");
