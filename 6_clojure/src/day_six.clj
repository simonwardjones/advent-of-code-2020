(ns day_six)

;; imports
(require '[clojure.string :as str])
(require '[clojure.set :as set])

;; load the data
(defn load_data []
  (slurp "day_two_data.txt"))

;; question 1
(defn get_sum_counts [data]
  (def groups (str/split data #"\n\n"))
  (def groups (map (fn [group] (str/replace group "\n" "")) groups))
  (reduce + (map count (map distinct groups))))

;; question 2
(defn get_sum_counts_all [data]
  (def groups (str/split data #"\n\n"))
  (def groups (map (fn [group] (map set (str/split group #"\n"))) groups))
  (def group_counts (map (fn [group] (count (reduce set/intersection group))) groups))
  (def answer (reduce + group_counts))
  answer)

;; main - call using `clj -X day_six/run`
(defn run [opts]
  (def data (load_data))
  (def question_one_answer (get_sum_counts data))
  (println "The sum of groups yes counts is: " question_one_answer)
  (def question_two_answer (get_sum_counts_all data))
  (println "The sum of groups all yes counts is: " question_two_answer))