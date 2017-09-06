module.exports = function (grunt) {
   grunt.initConfig({
      browserify: {
         dist: {
            options: {
               transform: [
                  [ "babelify",
                    {presets: ['es2015', 'react']}]
               ]
            },
            src: [
                "./my_site_django/src/government_audit/audit_search.react.js",
                "./my_site_django/src/government_audit/main.react.js"],
            dest: "./my_site_django/static/government_audit/audit_search.js"
         }
      },
      watch: {
         scripts: {
            files: ["./my_site_django/src/**/*.js"],
            tasks: ["browserify"]
         }
      }
   });

   grunt.loadNpmTasks("grunt-browserify");
   grunt.loadNpmTasks("grunt-contrib-watch");

   grunt.registerTask("default", ["watch"]);
   grunt.registerTask("build", ["browserify"]);
};
