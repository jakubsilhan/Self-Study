;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-reader.ss" "lang")((modname Cviceni4_trees_sorting) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
; 1) Zip merge of lists
(define (zip L1 L2)
  (cond
    [(empty? L1) L2]
    [(empty? L2) L1]
    [else (append (list (car L1) (car L2)) (zip (cdr L2) (cdr L1)))] ; can also take just one element at a time
  )
)

(zip (list 1 3 5) (list 2 4 6))

; 2) Sum larger numbers from second list
(define (sectivetsi L1 L2)
  (cond
    [(empty? L1) '()]
    [else (cons (suma_vetsich (car L1) L2) (sectivetsi (cdr L1) L2))]
  )
)

(define (suma_vetsich N List)
  (cond
    [(empty? List) 0]
    [(> (car List) N) (+ (car List)
                         (suma_vetsich N (cdr List))
                      )]
    [else (suma_vetsich N (cdr List))]
  )
)

(suma_vetsich 15 '(10 20 30 5))
(sectivetsi  '(15 8 35) '(10 20 30 5))

; Binary trees - definition
(define-struct  uzelBVS  (klic  levy  pravy))
(define testovaci
    (make-uzelBVS 20
        (make-uzelBVS 15
            (make-uzelBVS 8
                '()
                (make-uzelBVS 12
                    '() '()))
            (make-uzelBVS 17 '() '()))
        (make-uzelBVS 52
            (make-uzelBVS 39
                (make-uzelBVS 24 '() '())
                '())
            (make-uzelBVS 60 '() '()))))

; 3) Calculate depth of tree

;hloubka: uzelBVS -> number
;returns the max depth of a tree
(define (hloubka strom)
  (cond
    [(empty? strom) 0]
    [else (+ 1 (max (hloubka (uzelBVS-levy strom))
                    (hloubka (uzelBVS-pravy strom))
               )
          )
    ]
  )
)

(hloubka testovaci)

; 4) linearize a tree
; linearizuj: uzelBVS -> list
; Translates a binary tree into a list of ascending values
(define (linearizuj strom)
  (cond
    [(empty? strom) '()]
    [else (append (linearizuj (uzelBVS-levy strom)) (list (uzelBVS-klic strom)) (linearizuj (uzelBVS-pravy strom)))]
  )
)

(linearizuj testovaci)

; 5) Calculate largest difference in depth in tree
; vyvazeni: uzelBVS -> number
; Calculates the max depth difference in a tree (can be used to check if tree is balanced)
(define (vyvazeni strom)
  (cond
    [(empty? strom) 0]
    [else (max (abs (- (hloubka (uzelBVS-levy strom))
                       (hloubka (uzelBVS-pravy strom))))
               (vyvazeni (uzelBVS-levy strom))
               (vyvazeni (uzelBVS-pravy strom))
)]))

(vyvazeni testovaci)

; 6) Check if BVS - dodelat
(define (jeBVS? strom)
  (jeSerazene? (linearizuj strom)))

(define (jeSerazene? list)
  (cond
    [(empty? (cdr list)) #t]
    [else (and (jeSerazene? (cdr list))
               (< (car list) (car (cdr list))))]))
 
(jeSerazene? '(1 3 2 4))

(jeBVS? testovaci)