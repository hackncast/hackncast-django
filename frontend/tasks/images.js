module.exports = function(gulp, sources, $) {
  "use strict";

  // Gulp extensions for Images
  var imagemin      = require('gulp-imagemin');

  /* Task optimize images */
  gulp.task('img', function(){
    return gulp.src(sources.img.origin)
      .pipe(imagemin(sources.img.settings.minify))
      .pipe(gulp.dest(sources.img.target))
      .pipe($.print(sources.log.created));
  });

  gulp.task('img-clean', function (cb) {
    $.del(sources.img.target  + '*', cb);
    return cb(null);
  });
};
