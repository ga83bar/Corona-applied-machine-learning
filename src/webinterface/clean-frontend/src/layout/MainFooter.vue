<template>
  <footer
    class="footer"
    :class="{ [`footer-${type}`]: type }"
    :data-background-color="backgroundColor"
  >
    <div class="container">
      <nav>
        <ul>
          <li>
            <a href="https://gitlab.ldv.ei.tum.de/ami2020/group11">
              Project on Gitlab
            </a>
          </li>
          <li>
            <a href="https://www.youtube.com/watch?v=oavMtUWDBTM">
              Project Video
            </a>
          </li>
         
        </ul>
      </nav>
      <div class="copyright">
        
        Developed within the scope of the Applied Machine Intelligence 2020 project at TUM.
        <p>UI created by using Vue Material Kit by <a href="https://www.creative-tim.com/" target="_blank">Creative Tim</a></p>
        
       
      </div>
    </div>
  </footer>
</template>
<script>
export default {
  props: {
    backgroundColor: String,
    type: String
  }
};
</script>
<style></style>
