from rcp import get_polls, get_poll_data
import time, requests

current_name = ""
url = "https://www.realclearpolitics.com/epolls/2020/president/us/" \
      "2020_democratic_presidential_nomination-6730.html#polls"
polls_channel_url = "INSERT SLACK APP WEBHOOK HERE"
dont_care_about = ["Gabbard", "Yang", "Steyer", "Spread"]

while True:
    # Get array of the most recent polls from the meta poll url (first is RCP avg)
    number_of_most_recent_polls = 1
    polls = get_poll_data(url)[0]['data'][:number_of_most_recent_polls + 1]

    # Check if the first poll name has changed, if so print its contents as well as current RCP average info
    new_name = polls[1]["Poll"]
    poll_reports = ["NEW POLL"]
    if new_name != current_name:
        current_name = new_name
        for poll in polls[1:]:  # Iterate through non-RCP polls
            poll_report = []
            care_about = {k: v for (k, v) in poll.items() if k not in dont_care_about}

            #  Compile data and to report array
            for k, v in care_about.items():
                poll_report.append(str(k) + ": " + str(v))
            joined_report = "\n".join(poll_report)
            poll_reports.append(joined_report)

        #  Make a separate report for the RCP average information
        rcp_poll_report = []
        care_about_rcp = {k: v for (k, v) in polls[0].items() if (k not in dont_care_about) and (k != "Sample")}
        for k, v in care_about_rcp.items():
            rcp_poll_report.append(str(k) + ": " + str(v))
        joined_rcp_report = "\n".join(rcp_poll_report)
        poll_reports.append(joined_rcp_report)

        #  Concatenate "NEW POLL" + non-RCP poll reports + RCP average report
        report = poll_reports[0] + '\n' + '\n\n'.join(poll_reports[1:]) + '\n'
        print(report)

        #  Format and send report to Slack webhook
        payload_str = "\"" + report + "\""
        data_object = '{"text":' + payload_str + '}'
        my_request_return = requests.post(polls_channel_url, data=data_object)

    #  Wait for 30 minutes before polling again
    time.sleep(1800)
