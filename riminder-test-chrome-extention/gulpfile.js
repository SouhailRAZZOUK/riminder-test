var gulp                = require('gulp'),
    sass                = require('gulp-sass'),
    gutil               = require('gulp-util'),
    pug                 = require('gulp-pug'),
    connect             = require('gulp-connect'),
    // del                 = require('del'),
    historyApiFallback  = require('connect-history-api-fallback');


gulp.task('sass', ['sass-components'], function() {
  return gulp.src('src/assets/styles/app.scss')
    .pipe( sass().on('error', sass.logError) )
    .pipe( gulp.dest('bin/assets/styles/') )
    .pipe( connect.reload() );    
});

gulp.task('sass-components', function() {
  return gulp.src('src/components/**/*.scss')
    .pipe( sass().on('error', sass.logError) )
    .pipe( gulp.dest('bin/components/') )
    .pipe( connect.reload() );    
});

gulp.task('js', ['js-components'], function() {
  return gulp.src('src/assets/scripts/**/*.js')
    .pipe( gulp.dest('bin/assets/js/'))
    .pipe( connect.reload() );
});

gulp.task('js-components', function() {
  return gulp.src('src/components/**/*.js')
    .pipe( gulp.dest('bin/components/'))
    .pipe( connect.reload() );
});

gulp.task('pug', function() {
  return gulp.src(['src/**/*.pug', '!src/includes/**/*','!src/fragments/**/*'])
    .pipe( pug({ pretty: true }).on('error', function(e) {gutil.log(e.message).beep();return;}))
    .pipe( gulp.dest('bin/'))
    .pipe( connect.reload() );
});

// gulp.task('clean', function () {
// 	del(['bin/**/*', '!bin/', '!bin/assets/components', '!bin/assets/components/**/*', '!bin/assets/js/**/*'], {force: true}).then(paths => {
//     if(paths.length != 0){
//       gutil.log('Files and folders that were deleted:\n', gutil.colors.orange(paths.join('\n')));
//     }
//   });
// });

gulp.task('watch', function () {
  gulp.watch('src/assets/styles/**/*.scss',['sass']);
  gulp.watch('src/components/**/*.scss',['sass-components']);

  gulp.watch('src/**/*.pug',['pug']);

  gulp.watch('src/assets/scripts/**/*.js',['js']);
  gulp.watch('src/components/**/*.js',['js-components']);
});

gulp.task('connect', ['watch'], function() {
	connect.server({
		root: "bin/",
    port: 3000,
		livereload: true,
    middleware: function(connect, opt) {
      return [historyApiFallback({
                index: '/index.html'
              })];
    }
	});
});

gulp.task('default', ['pug','sass','js','connect']);