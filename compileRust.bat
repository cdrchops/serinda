cd src/rust
cargo build --release
cd ../..
@REM # if linux copy the so
@REM #cp src/rust/target/release/libserindalib.dylib ./mylibserindalib.so

@REM  if windows copy the dll to the lib directory
cp src/rust/target/release/serindalib.dll ./build/serindalib.dll