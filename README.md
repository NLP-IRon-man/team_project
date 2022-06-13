# Natural Language Processing and Information Retrieval
Team 7 IRon man

## Main idea

Show each character’s emotional change using graph.

<img src="https://user-images.githubusercontent.com/48765232/173276457-a20f386e-8f26-452d-a524-19215b44159e.png" alt="Joker" width="40%" heigh="40%" />

1. Crawling the scripts and divide scripts by characters, and find 5 main characters.
2. Analyze the movie scripts divided into 5 parts.
3. Analyze 7 emotions(disgust, surprise, neutral, anger, sad, happy, fear) changing from start to end of the movie
4. Users can search movies and see what they want.


<img alt="Main-Idea" src="https://user-images.githubusercontent.com/48765232/173276908-046c7f71-85be-4d2e-ae91-7477c8a617fb.png" width="70%" heigh="70%"/>

## Architecture

<img alt="architecture" src="https://user-images.githubusercontent.com/48765232/173277242-63781af0-5bc4-4317-b013-76fbf615c3ea.png" width="70%" heigh="70%"/>

1. Crawl movie scripts from IMSDB. While crawling, divide the script person by person using an HTML tag.
2. Figure 5 main characters from each movie. As we mentioned last presentations, we used 3 scores to figure main characters.
    1. Someone who talks much. 
    2. Someone who talks frequently. 
    3. Someone who is mentioned by other characters many times.
3. Preprocess script by removing stop words.
4. Analyze emotions using the word-emotion dataset. Some work on datasets like normalization. Divide the movie into 5 periods for each character.
5. Draw an emotional change chart for 5 characters and save images to the database


## Example

- #### Input

  Joker(2019)
  
  <img src="https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg" alt="Movie" width="30%" height="30%" />  


- #### Output:
  
  Joker(2019)
  
  <img src="https://user-images.githubusercontent.com/48765232/173278443-3a423d38-d225-4475-833e-fe9c6124dba8.png" alt="WebPageAll" width="30%" height="30%" /> 
  
  <img src="https://user-images.githubusercontent.com/48765232/173276457-a20f386e-8f26-452d-a524-19215b44159e.png" alt="Joker" width="40%" heigh="40%"/> <img src="https://user-images.githubusercontent.com/48765232/173277035-93858c92-a073-4342-96bb-f1f0c10fafd3.png" alt="Joker" width="40%" heigh="40%"/> 
  
  Cast Away(2000)
  
  <img src="https://user-images.githubusercontent.com/48765232/173277124-ad3cda48-81b3-4ec6-926f-7bbea996fc36.png" alt="castaway" width="40%" heigh="40%" /> 
  
  
## Evaluation

Not easy to evaluate our program.
1. Emotion is personal area
2. It’s hard to apply existed test set which has [text : emotion] format because our data text is much longer, and we want to analyze 7 emotions, not one emotion.

So we decided to select some popular movies and evaluate them.
If most people agree with the result, it seems successful.


## Improvement

1. Our program is fast but doesn’t care about context.
   - Using ML models can solve this but it is slower. Precision & Speed are trade-off.
2. Movie characters don’t really talk enough to analyze emotion.
   - Hard to figure exact emotion by analyzing short conversation.
3. Our program can’t figure time concept.
   - For example, in “Cast-away”, the main character frequently thinks about the past. But our program can’t know the text is talking about past. So the emotion graph seems unstable.


## Team

#### Team leader

- Seongchan Cho

#### Team member 

- Byungjun Kim

- Seuyoon Joo

  
