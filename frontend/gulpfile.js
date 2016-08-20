var gulp         = require('gulp');
var less         = require('gulp-less');
var watch        = require('gulp-watch');
var minifyCSS    = require('gulp-minify-css');
var rename       = require('gulp-rename');
var replace      = require('gulp-replace');
var print        = require('gulp-print');
var autoprefixer = require('gulp-autoprefixer');
var cache        = require('gulp-cache');
var debug        = require('gulp-debug');
var duration     = require('gulp-duration');
var imagemin     = require('gulp-imagemin');
var include      = require("gulp-include");
var uglify       = require('gulp-uglify');
var del          = require('del');
var browserSync  = require('browser-sync').create();

log = {
  created: function(file) {
    return 'Created: ' + file;
  }
}

settings = {
  prefix: {
    browsers: [
      'last 2 versions',
      '> 1%',
      'opera 12.1',
      'bb 10',
      'android 4'
    ]
  }
}

/* Task to compile less */
gulp.task('css', function() {
  gulp.src(['./src/less/**/*.less'])
    .pipe(less())
    .pipe(autoprefixer(settings.prefix))
    .pipe(gulp.dest('./dist/semantic/custom'))
    .pipe(print(log.created))
    .pipe(minifyCSS({
      processImport       : false,
      restructuring       : false,
    }))
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest('./dist/semantic/custom'))
    .pipe(print(log.created))
    .pipe(duration('Elapsed time'))
  ;
});

/* Task optimize images */
gulp.task('img', function(){
  return gulp.src('./src/img/**/*.+(png|jpg|gif|svg)')
  .pipe(cache(imagemin({
    interlaced: true,
    pngquant: true,
    progressive: true
  })))
  .pipe(gulp.dest('./dist/img/'))
  .pipe(print(log.created))
});

/* Task copy vendor files */
gulp.task('vendor', function(){
  return gulp.src(['./src/vendor/**/*'])
  .pipe(gulp.dest('./dist/'))
});

/* Task that compiles js files */
gulp.task('js', function(){
  return gulp.src(['./src/js/**/*.js'])
  .pipe(include({
    includePaths: [
      __dirname
    ]
  })).on('error', console.log)
  .pipe(gulp.dest("./dist/js"))
  .pipe(print(log.created))
  .pipe(uglify())
  .pipe(rename({suffix: '.min'}))
  .pipe(gulp.dest("./dist/js"))
  .pipe(print(log.created));
});

/* Task to watch less changes */
gulp.task('watch', function() {
  browserSync.init({
    proxy: "localhost:8000",
    open: false
  })

  gulp.watch(
      ['./src/less/**/*.less', './dist/semantic/**/*.css'], ['css']
  ).on('change', browserSync.reload);

  gulp.watch(
    ['./src/js/**/*.js', './dist/semantic/**/*.js'], ['js']
  ).on('change', browserSync.reload);

  gulp.watch(
    ['./src/img/**/*.+(png|jpg|gif|svg)'], ['img']
  ).on('change', browserSync.reload);

  gulp.watch(
    ['../templates/dj/**/*.html', '../templates/**/*.jinja']
  ).on('change', browserSync.reload);
});

/* Clean output and cache */
gulp.task('frontend-clean', function (cb) {
  del('./dist/*', cb)
  return cache.clearAll(cb);
});

/* Task when running `gulp` from terminal */
gulp.task('default', ['vendor', 'css', 'js', 'img']);
