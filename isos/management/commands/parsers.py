from bs4 import BeautifulSoup


def get_summary_and_advice(summary):
    soup = BeautifulSoup(summary, 'lxml')
    summary_tag = soup.find('b', text='TRAVEL RISK SUMMARY')
    if not summary_tag:
        summary_tag = soup.find('b', text='TRAVEL RISK')
    travel_risk_summary = []
    for elem in summary_tag.next_siblings:
        if elem.text == 'STANDING TRAVEL ADVICE' or elem.name == 'a':
            break
        travel_risk_summary.append(str(elem))
    standing_advice_tag = soup.find('b', text='STANDING TRAVEL ADVICE')
    travel_advice = []
    for elem in standing_advice_tag.next_siblings:
        if elem.text == 'RISK ZONES' or elem.name == 'a':
            break
        travel_advice.append(str(elem))
    return '\n'.join(travel_risk_summary), '\n'.join(travel_advice)


def get_content(contents, text):
    soup = BeautifulSoup(contents, 'lxml')
    search_tag = soup.find('b', text=text)
    info = [str(search_tag)]
    for elem in search_tag.next_siblings:
        info.append(str(elem))
    return '\n'.join(info)


def get_calendar(contents):
    soup = BeautifulSoup(contents, 'lxml')
    search_tag = soup.find('div', class_='contentBox').find('div', class_='contentMiddle').find('span')
    info = []
    for e in search_tag.findAll('br'):
        e.extract()
    for elem in search_tag.contents:
        info.append(str(elem))
    return '\n'.join(info)


def get_getting_there(content):
    soup = BeautifulSoup(content, 'lxml')
    tag = soup.find(
        id='ctl00_CountryGuideContentPlaceHolder_ucCGGettingThere_spanGettingThere')
    getting_there = []
    for elem in tag.contents:
        getting_there.append(str(elem))
    return '\n'.join(getting_there)


def get_getting_around(contents):
    soup = BeautifulSoup(contents, 'lxml')
    search_tag = soup.find('b', text='BY AIR')
    if not search_tag:
        search_tag = soup.find('b', text='BY ROAD')
    info = [str(search_tag)]
    for elem in search_tag.next_siblings:
        info.append(str(elem))
    return '\n'.join(info)


def get_phone_and_power(content):
    soup = BeautifulSoup(content, 'lxml')
    tag = soup.find(
        id='ctl00_CountryGuideContentPlaceHolder_ucCGVoltageAndPlug_spanVoltageAndPlugs')
    phone_and_power = []
    for elem in tag.contents:
        phone_and_power.append(str(elem))
    return '\n'.join(phone_and_power)


def get_cultural_tips(contents):
    soup = BeautifulSoup(contents, 'lxml')
    businesswomen_tag = soup.find(text='Tipping')
    span = businesswomen_tag.find_parent('span')
    cultural_tips = [str(span)]
    for elem in span.contents:
        if elem.text:
            cultural_tips.append(str(elem))
    return '\n'.join(cultural_tips)


def get_medical(contents):
    soup = BeautifulSoup(contents, 'lxml')
    search_tag = soup.find(id="Before You Go")
    advice = []
    for elem in search_tag.next_siblings:
        if elem.name == 'table':
            break
        advice.append(str(elem))

    vaccination_tag = soup.find(
        id='vaccinations').find_parent('td').find_parent('tr')
    vaccinations = []
    for elem in vaccination_tag.next_siblings:
        if 'More on diseases' in elem.text:
            break
        vaccinations.append(str(elem))

    malaria_tag = soup.find(text='Malaria').find_parent('td').find_parent('tr')
    diseases = []
    for elem in malaria_tag.next_siblings:
        diseases.append(str(elem))

    return '\n'.join(advice), '\n'.join(vaccinations), '\n'.join(diseases)


def get_risk_ratings(contents):
    soup = BeautifulSoup(contents, 'lxml')
    all_tds = soup.find(id='ctl00_CountryGuideContentPlaceHolder_ucCGCGLanding_ucCGRiskRatings_divRiskRating').find_all('td')
    medical_risk = all_tds[0].text.strip().split(' ')
    travel_risk = all_tds[1].text.strip().split(' ')
    return medical_risk[0], travel_risk[0]
