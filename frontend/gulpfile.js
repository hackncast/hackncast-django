var del           = require('del');
var gulp          = require('gulp');
var pump          = require('pump');
var print         = require('gulp-print');
var watch         = require('gulp-watch');
var rename        = require('gulp-rename');
var browserSync   = require('browser-sync').create();
var sourcemaps    = require('gulp-sourcemaps');


// Load Gulp settings
var sources = require('./tasks/settings.json');

// Initialize shared plugins map
var plugins  = {
  rename: rename,
  sourcemaps: sourcemaps,
  print: print,
  pump: pump,
  del: del
};

// Functions and variables
sources.js.settings.include.includePaths = [__dirname];
sources.log = {
  created: function(file) {
    return 'Created: ' + file;
  }
};

// Inicialize tasks
require('./tasks/images.js')(gulp, sources, plugins);
require('./tasks/javascript.js')(gulp, sources, plugins);
require('./tasks/less.js')(gulp, sources, plugins);

/* Task that copy fonts */
gulp.task('fonts', function(){
  return gulp.src(sources.fonts.origin)
    .pipe(gulp.dest(sources.fonts.target))
    .pipe(print(sources.log.created));
});

gulp.task('fonts-clean', function (cb) {
  del(sources.fonts.target  + '*', cb);
  return cb(null);
});

/* Task to watch changes */
gulp.task('watch', function(cb) {
  browserSync.init(sources.browsersync);
  gulp.watch(sources.less.origin, ['css']);
  gulp.watch(sources.less.minify).on('change', browserSync.reload);

  gulp.watch(sources.js.origin, ['js']);
  gulp.watch(sources.js.minify).on('change', browserSync.reload);

  gulp.watch(sources.img.origin, ['img']);
  gulp.watch(sources.img.target + '**/*', ['img']).on('change', browserSync.reload);

  gulp.watch(sources.templates.origin).on('change', browserSync.reload);

  gulp.watch(sources.python.origin).on('change', function(){
    setTimeout(browserSync.reload, 3000);
  });

  cb(null);
});

gulp.task('clean', ['img-clean', 'js-clean', 'css-clean']);
gulp.task('dist', ['img', 'js-dist', 'css-dist']);
gulp.task('default', ['clean', 'fonts', 'img', 'js', 'css']);
