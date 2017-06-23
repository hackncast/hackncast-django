module.exports = function(gulp, sources, $) {
  "use strict";

  // Gulp extensions for JS
  var jshint        = require('gulp-jshint');
  var uglify        = require('gulp-uglify');
  var include       = require("gulp-include");
  var babel         = require("gulp-babel");

  /* Task that checks JS syntax */
  gulp.task('js-hint', function(){
    return gulp.src(sources.js.origin)
      .pipe(jshint())
      .pipe(jshint.reporter('jshint-stylish'));
  });

  /* Task that compiles js files */
  gulp.task('js', function(){
    return gulp.src(sources.js.origin)
      .pipe(include(sources.js.settings.include)).on('error', console.log)
      .pipe(gulp.dest(sources.js.target))
      .pipe($.print(sources.log.created));
  });

  /* Task that minify js files */
  gulp.task('js-min', ['js'], function(cb){
    $.pump([
        gulp.src(sources.js.minify),
        $.sourcemaps.init(),
        babel(sources.js.settings.babel),
        uglify(),
        $.rename({suffix: '.min'}),
        $.sourcemaps.write('./'),
        gulp.dest(sources.js.target),
        $.print(sources.log.created),
      ],
      cb
    );
  });

  gulp.task('js-clean', function (cb) {
    $.del(sources.js.target  + '*', cb);
    return cb(null);
  });

  gulp.task('js-dist', ['js-clean', 'js-min']);
};
