module.exports = function (grunt) {
   grunt.initConfig({
      browserify: {
         dist: {
            options: {
               transform: [
                  [ "babelify",
                    {loose: "all"},
                    {presets: ['es2015', 'react']}]
               ]
            },
            files: {
               // if the source file has an extension of es6 then
               // we change the name of the source file accordingly.
               // The result file's extension is always .js
               "./my_site_django/static/government_audit/audit_search.js":
                 ["./my_site_django/src/government_audit/audit_search.js"]
            }
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