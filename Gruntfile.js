module.exports = function(grunt) {
  // All JS goes into a single file, ordering doesn't matter.
  const jsSrc = "my_site_django/src/**/*.js";
  const jsDest = "my_site_django/static/min.js";

  // CSS must be kept separate and ordered.
  const mainCssSrc = [
    "my_site_django/src/css/my_site_django/bootstrap.min.css",
    "my_site_django/src/css/my_site_django/font-awesome.min.css",
    "my_site_django/src/css/my_site_django/clean-blog.css"
  ];
  const mainCssDest = "my_site_django/static/min.css";
  const auditCssSrc = "my_site_django/src/css/government_audit/audit_search.css";
  const auditCssDest = "my_site_django/static/government_audit/min.css";

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    clean: ['my_site_django/static/**/*.js',
      'my_site_django/static/**/*.css'
    ],
    concat: {
      options: {separator: '\n'},
      css: {
        files: {
          [mainCssDest]: mainCssSrc,
          [auditCssDest]: auditCssSrc,
        },
      }
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
        src: jsSrc,
        dest: jsDest
      }
    },
    uglify: {
      options: {banner: '/*\n <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> \n*/\n'},
      build: {
        src: jsDest,
        dest: jsDest,
      }
    },
    cssmin: {
      options: {banner: '/*\n <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> \n*/\n'},
      dist: {
        files: {
          [mainCssDest]: mainCssSrc,
          [auditCssDest]: auditCssSrc,
        }
      }
    },
    watch: {
      scripts: {
        files: [jsSrc, mainCssSrc, auditCssSrc],
        tasks: ["clean", "browserify", "concat:css"]
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
