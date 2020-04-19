load harness

@test "mytest-1" {
  check 'x := 1' '{x → 1}'
}

@test "mytest-2" {
   check 'i := 5 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }' '{fact → 120, i → 0}'
}

@test "mytest-3" {
   check 'i := 5 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }' '{fact → 120, i → 0}'
}

@test "mytest-4" {
   check 'i := 5 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }' '{fact → 120, i → 0}'
}

@test "mytest-5" {
 check 'i := 5 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }' '{fact → 120, i → 0}'
}



