module.exports = function(grunt) {
  const auditJsSrc = [
    "my_site_django/src/js/government_audit/**/*.js",
    "!my_site_django/src/js/government_audit/**/*.test.js*"];
  const auditJsDest = "my_site_django/static/government_audit/min.js";

  const auditCssSrc = "my_site_django/src/css/government_audit/audit_search.css";
  const auditCssDest = "my_site_django/static/government_audit/min.css";

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    clean: ['my_site_django/static/**/*.js',
      'my_site_django/static/**/*.css'
    ],
    concat: {
      options: {separator: '\n'},
      files: {
        src: auditCssSrc,
        dest: auditCssDest
      },
    },
    browserify: {
      options: {
        transform: [
          ["babelify",
            {
              presets: [
                'es2015',
                'react'
              ]
            }
          ]
        ]
      },
      files: {
         src: auditJsSrc,
         dest: auditJsDest
      },
    },
    uglify: {
      options: {banner: '/*\n <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> \n*/\n'},
      files: {
        src: auditJsSrc,
        dest: auditJsDest
      }
    },
    cssmin: {
      options: {banner: '/*\n <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> \n*/\n'},
      files: {
        src: auditCssSrc,
        dest: auditCssDest
      },
    },
    watch: {
      scripts: {
        files: [auditJsSrc, auditCssSrc],
        tasks: ["clean", "browserify", "concat"]
      }
    }
  });

  grunt.loadNpmTasks("grunt-browserify");
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks("grunt-contrib-watch");

  grunt.registerTask("default", ["watch"]);
  grunt.registerTask("prod", ["clean", "browserify", "uglify", "cssmin"]);
};
