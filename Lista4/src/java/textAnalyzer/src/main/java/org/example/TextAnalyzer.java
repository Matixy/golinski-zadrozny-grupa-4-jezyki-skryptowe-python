package org.example;

import com.fasterxml.jackson.databind.ObjectMapper; // external library for parsing Object to JSON

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

public class TextAnalyzer {
  // attributes
  private Path filePath;

  // record- Data Transfer Object
  public record TextStatistics(
    String path,
    long chars,
    long words,
    long lines,
    char mostFrequentChar,
    String mostFrequentWord
  ) {}

  // constructors
  public TextAnalyzer(String filePathStr) {
    this.filePath = Paths.get(filePathStr);
  }

  // public methods
  public TextStatistics analyze() throws Exception {
    // handle errors
    if (!Files.exists(filePath) || !Files.isRegularFile(filePath)) {
      throw new IllegalAccessException("File not found or not a text file!");
    }

    return analyzeText();
  }

  public String toJson(TextStatistics stats) {
    try {
      ObjectMapper mapper = new ObjectMapper();
      // mapper changing TextStatistic with json string
      return mapper.writerWithDefaultPrettyPrinter().writeValueAsString(stats);
    } catch (Exception e) {
      throw new RuntimeException("Error while converting to JSON: ", e);
    }
  }

  // private methods
  private TextStatistics analyzeText() throws IOException {
    // read whole file
    String fullText = Files.readString(filePath);
    fullText = fullText.replace("\r\n", "\n"); // standard text if user runs program on windows

    // create textStats record
    long charCount = fullText.length();
    long wordCount = 0;
    long lineCount = 0;

    if (!fullText.isEmpty()) {
      lineCount = fullText.split("\n", -1).length; // split text for new line separators
    }

    // prepare helper structures
    Map<Character, Long> charFreq = new HashMap<>();
    Map<String, Long> wordFreq = new HashMap<>();

    // analyze chars
    for (char c : fullText.toCharArray()) {
      if (!Character.isWhitespace(c)) {
        char lowerChar = Character.toLowerCase(c);
        charFreq.put(lowerChar, charFreq.getOrDefault(lowerChar, 0L) + 1L);
      }
    }

    //analyze words
    String[] words = fullText.split("[^\\p{L}]+"); // split after any which is not letter (like .isalpha())
    for (String word : words) {
      if (!word.isEmpty()) {
        wordCount++;
        String lowerWord = word.toLowerCase();
        wordFreq.put(lowerWord, wordFreq.getOrDefault(lowerWord, 0L) + 1L);
      }
    }

    return new TextStatistics(
            filePath.toString(),
            charCount,
            wordCount,
            lineCount,
            findMostFrequentChar(charFreq),
            findMostFrequentWord(wordFreq)
    );
  }

  private char findMostFrequentChar(Map<Character, Long> map) {
    long max = 0;
    char bestChar = '\0';

    for (Map.Entry<Character, Long> entry : map.entrySet()) { // Map.entry : map.entrySet provides single key, value elem from map
      if (entry.getValue() > max) {
        max = entry.getValue();
        bestChar = entry.getKey();
      }
    }

    return bestChar;
  }

  private String findMostFrequentWord(Map<String, Long> map) {
    long max = 0;
    String bestWord = "";

    for (Map.Entry<String, Long> entry : map.entrySet()) { // Map.entry : map.entrySet provides single key, value elem from map
      if (entry.getValue() > max) {
        max = entry.getValue();
        bestWord = entry.getKey();
      }
    }

    return bestWord;
  }

  // setters & getters
  public Path getFilePath() {
    return filePath;
  }

  public void setFilePath(Path filePath) {
    this.filePath = filePath;
  }
}
