import streamlit, sys, json, requests

URL = 'https://api.sampleapis.com/futurama/'
ENDPOINTS = {
    'Information': 'info',
    'Characters': 'characters',
    'Cast': 'cast',
    'Episodes': 'episodes',
    'Questions': 'questions',
    'Inventory': 'inventory'
}


def load_content(option):
    r = requests.get(URL + ENDPOINTS[option])
    if r:
        content = json.loads(r.content)
    else:
        print("ERROR: Request failed.")
        sys.exit(1)

    match option:
        case 'Information':
            # Only one object returned
            handle = content[0]
            streamlit.subheader('Synopsis')
            streamlit.write(handle['synopsis'])
            # Subheader is not a variadic function, concatenate the argument
            streamlit.subheader('Years aired: ' + handle['yearsAired'])
            streamlit.subheader('Creators')
            for creator in handle['creators']:
                name = creator['name']
                # Name as a hyperlink to IMDb page
                hyperlink = f"[{name}](%s)" % creator['url']
                streamlit.markdown(f"- {hyperlink}")

        case 'Characters':
            # Character iterable as a handle
            for character in content:
                base = character['name']
                full_name = f"{base['first']} {base['middle']} {base['last']}"
                streamlit.subheader(full_name)
                streamlit.image(character['images']['main'])
        case 'Cast':
            for person in content:
                name = person['name']
                hyperlink = f"[{name}](%s)" % person['bio']['url']
                streamlit.subheader(hyperlink)
                streamlit.write('Born:', person['born'])
                if person['died']:
                    streamlit.write('Write:', person['died'])
        case 'Episodes':
            streamlit.write(content)
            for episode in content:
                streamlit.subheader('Episode ' + episode['number'] + ':')
                streamlit.write('**Title:**', episode['title'])
                streamlit.write('**Writers:**', episode['writers'])
                streamlit.write('**Original Air Date:**', episode['originalAirDate'])
                streamlit.write(episode['desc'])
        case 'Questions':
            streamlit.subheader('Quiz')
            for question in content:
                answer = streamlit.radio(
                    question['question'],
                    question['possibleAnswers'],
                    index=None
                )
                if answer == question['correctAnswer']:
                    streamlit.write(':green[Your answer is correct!]')
                elif answer and answer != question['correctAnswer']:
                    streamlit.write(':red[Your answer is incorrect!]')
                
        case 'Inventory':
            for item in content:
                streamlit.subheader(item['title'])
                streamlit.write('**Category:**', item['category'])
                streamlit.write(item['description'])
                if item['slogan']:
                    streamlit.write('**Slogan:**', item['slogan'])
                streamlit.write('**Price:**', item['price'])
                streamlit.write('**Stock:**', item['stock'])

    
def main():
    streamlit.title('LW4. REST client')
    option = streamlit.selectbox(
        'Choose available endpoint:',
        ENDPOINTS.keys(),
        index=None,
        placeholder='Pick one from here...'
    )
    if option:
        load_content(option)

if __name__ == '__main__':
    main()
