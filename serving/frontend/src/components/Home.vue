<template>
  <div class="page-wrapper">
    <div class="header-wrapper">
      <div class="header">
        Pinkoff Travel
      </div>
      <div v-if="!this.enoughOutlined() && !recommended">
        Choose at least {{ requiredItems }} landmarks:
      </div>
      <div v-if="recommended">
        Based on our data, people like you might also like these landmarks:
      </div>
      <v-btn class="btn-recommend" elevation="2" rounded :loading=this.loading v-on:click="this.onRecommend" v-if="this.enoughOutlined() && !recommended">Recommend</v-btn>
      <v-btn class="btn-recommend" elevation="2" rounded disabled v-else>Recommend</v-btn>
    </div>
    <div class="main-wrapper">

      <div class="gallery-container" v-if="!this.recommended">
        <stack :column-min-width="320" :gutter-width="20" :gutter-height="20" ref="stack">
          <stack-item :key="item.item_id" v-for="item in items">
            <v-card class="mx-auto" width="400" :height="cardHeight(item)" :outlined=item.outlined v-on:click="item.outlined^=true;">
              <v-img :src="item.url" :lazy-src="item.lazy_url" :height="item.height" width=400></v-img>
              <v-card-title>
                {{ item.subtitle }}
              </v-card-title>
<!--               <v-card-subtitle>
                {{ item.subtitle }}
              </v-card-subtitle> -->
            </v-card>
          </stack-item>
        </stack>
      </div>

      <div class="gallery-container" v-if="this.recommended">
        <stack :column-min-width="320" :gutter-width="20" :gutter-height="20" ref="stack_recommended">
          <stack-item :key="item.item_id" v-for="item in recommended_items">
            <v-card class="mx-auto" width="400" :height="cardHeight(item)">
              <v-img :src="item.url" :lazy-src="item.lazy_url" :height="item.height" width=400></v-img>
              <v-card-title>
                {{ item.subtitle }}
              </v-card-title>
<!--               <v-card-subtitle>
                {{ item.subtitle }}
              </v-card-subtitle> -->
            </v-card>
          </stack-item>
        </stack>
      </div>

    </div>
  </div>
</template>

<script>
import { Stack, StackItem } from 'vue-stack-grid'
import axios from 'axios'

export default {
  name: 'Home',
  data () {
    return {
      items: [],
      recommended_items: [],
      loading: false,
      requiredItems: 5,
      baseWidth: 400,
      recommended: false,
    }
  },
  components: {
    Stack,
    StackItem
  },
  created: function() {
      axios.get('/api/options').then(response => {
          this.items = response.data.items;
          setTimeout(() => { this.$refs.stack.reflow(); }, 200);
      })
  },
  methods: {
    enoughOutlined: function () {
      let res = 0
      for (let item of this.items) {
        res += item.outlined
      }
      return res >= this.requiredItems
    },
    onRecommend: function (event) {
      if (this.recommended) {
        return;
      }
      this.loading = true;
      var visited_items = [];

      this.items.forEach((item) => {
        if (item.outlined) {
          visited_items.push(item.item_id);
        }
      });

      console.log(visited_items);

      axios.post('/api/recommend', visited_items).then((response) => {
        this.loading = false;
        this.recommended_items = response.data.items;
        this.recommended = true;
        console.log(response);
        setTimeout(() => { this.$refs.stack_recommended.reflow(); }, 100);
        setTimeout(() => { this.$refs.stack_recommended.reflow(); }, 200);
        setTimeout(() => { this.$refs.stack_recommended.reflow(); }, 500);
        setTimeout(() => { this.$refs.stack_recommended.reflow(); }, 1000);
        setTimeout(() => { this.$refs.stack_recommended.reflow(); }, 2000);
        setTimeout(() => { this.$refs.stack_recommended.reflow(); }, 5000);
      })
    },
    cardHeight: function (item) {
      return item.height + 60
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.header-wrapper {
  display: flex;
  justify-content: space-between;
  height: 64px;
  background: white;
  align-items: center;
  padding-left: 32px;
  box-shadow: 0 0 64px rgba(0, 0, 0, 0.2);
  position: fixed;
  z-index: 10;
  width: 100%;
}

.header {
  font-size: 1rem
}

h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.v-sheet--outlined {
  border: 2px solid blue !important;
}

.gallery {
  margin: 32px;
  display: flex;
  flex-direction: column;
  flex-flow: row wrap;
  justify-content: space-between;
}

.gallery-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: 32px;
}

.page-wrapper {
  display: flex;
  flex-flow: column;
}

.btn-recommend {
  margin: 32px !important;
  background-color: #ffdd2d !important;
  color: black !important;
  font-family: inherit;
}

.v-progress-linear__indeterminate .short {
  background-color: black !important;
}

.main-wrapper {
  margin-top: 64px;
}

</style>
