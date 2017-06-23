module.exports = function(gulp, sources, $) {
  "use strict";

  // Gulp extensions for Less/CSS
  var less          = require('gulp-less');
  var lesshint      = require('gulp-lesshint');
  var cleanCSS      = require('gulp-clean-css');
  var autoprefixer  = require('gulp-autoprefixer');

  gulp.task('css-hint', function() {
    return gulp.src(sources.less.origin)
      .pipe(lesshint({}))
      .pipe(lesshint.reporter())
      .pipe(lesshint.failOnError());
  });

  /* Task to compile less */
  gulp.task('css', function() {
    return gulp.src(sources.less.origin)
      .pipe(less())
      .pipe(autoprefixer(sources.less.settings.prefix))
      .pipe($.print(sources.log.created))
      .pipe(gulp.dest(sources.less.target))
    ;
  });

  gulp.task('css-min', ['css'], function(cb) {
    $.pump([
        gulp.src(sources.less.minify),
        $.sourcemaps.init(),
        cleanCSS(sources.less.settings.minify),
        $.rename({suffix: '.min'}),
        $.sourcemaps.write('./'),
        $.print(sources.log.created),
        gulp.dest(sources.less.target),
      ],
      cb
    );
  });

  gulp.task('css-clean', function (cb) {
    $.del(sources.less.target  + '*');
    return cb(null);
  });

  gulp.task('css-dist', ['css-clean', 'css-min']);
};
