package org.example;

import java.util.Scanner;

public class App {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);

    if (!scanner.hasNextLine()) {
      System.err.println("Error: no input file provided");
      System.exit(1);
    }

    String filePathString = scanner.nextLine().trim();

    // analyze file
    TextAnalyzer analyzer = new TextAnalyzer(filePathString);

    try {
      TextAnalyzer.TextStatistics stats = analyzer.analyze();
      // get json and print it
      System.out.println(analyzer.toJson(stats));
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
