<template>
  <div class="background">
    <md-menu md-direction="bottom-start" md-align-trigger>
      <md-button md-menu-trigger>Align with trigger - clickable</md-button>

      <md-menu-content>
        <md-menu-item @click="click1">My Item 1</md-menu-item>
        <md-menu-item @click="click2">My Item 2</md-menu-item>
        <md-menu-item @click="click3">My Item 3</md-menu-item>
      </md-menu-content>
    </md-menu>

    <md-menu md-direction="bottom-end">
      <md-button md-menu-trigger>Bottom End</md-button>

      <md-menu-content>
        <md-menu-item >My Item 1</md-menu-item>
        <md-menu-item>My Item 2</md-menu-item>
        <md-menu-item>My Item 3</md-menu-item>
      </md-menu-content>
    </md-menu>

  </div>
</template>

<script>
  export default {
    name: 'Directions'
  }
</script>

<style>
  .md-menu {
    margin: 24px;
  }
  .background{
      background-color: darkgray;
  }
</style>