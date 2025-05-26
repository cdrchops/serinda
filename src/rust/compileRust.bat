REM TODO: AUTOMATE THIS SO THAT ONLY ONE FILE GETS EDITED THEN THE OTHER ONE GETS COPIED AND PIECES CHANGED
REM       SUCH AS # TO REM AND libserindalib.dylib to serindalib.dll etc and os independent slashes
REM THIS COULD ALSO BE DONE IN PYTHON AND NOT CALL A SCRIPT
rem cd src/rust
cargo build --release
rem cd ../..
REM if linux copy the so
REM cp src/rust/target/release/serindalib.dylib ./build/serindalib.so

REM if windows copy the dll to the lib directory
rem copy .\src\rust\target\release\serindalib.dll .\build\serindalib.dll