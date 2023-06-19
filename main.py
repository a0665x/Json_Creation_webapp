import streamlit as st
import json
from json_graph import show_Json_graph


# Create a session state object
if 'session_state' not in st.session_state:
    st.session_state['session_state'] = {"resources":[], "ads":[], "talks":[], "routes":[], "localizations":[], "parts":[], "guides":[]}

def main():
    global data
    # Create a sidebar menu
    menu = ["Home", "資源設定", "廣告設定", "⽂本設定", "路線設定", "本地化設定", "段落設定", "導覽點設定", "Generate JSON"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Based on the user's choice, show the corresponding page
    if choice == "Home":
        show_home()
    elif choice == "資源設定":
        show_resources()
    elif choice == "廣告設定":
        show_ads()
    elif choice == "⽂本設定":
        show_talks()
    elif choice == "路線設定":
        show_routes()
    elif choice == "本地化設定":
        show_localizations()
    elif choice == "段落設定":
        show_parts()
    elif choice == "導覽點設定":
        show_guides()
    elif choice == "Generate JSON":
        generate_json()

    # Upload the json file
    uploaded_file = st.sidebar.file_uploader("Upload local JSON", type=['json'])

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # To read the file as a string:
        string_data = uploaded_file.read().decode("utf-8")
        # To convert the string data to JSON:
        json_data = json.loads(string_data)


        st.session_state['session_state']["resources"]=json_data["資源設定 (resources)"]
        st.session_state['session_state']["ads"]=json_data["廣告設定 (ads)"]
        st.session_state['session_state']["talks"]=json_data["⽂本設定 (talks)"]
        st.session_state['session_state']["routes"]=json_data["路線設定 (routes)"]
        st.session_state['session_state']["localizations"]=json_data["本地化設定 (localizations)"]
        st.session_state['session_state']["parts"]=json_data["段落設定 (parts)"]
        st.session_state['session_state']["guides"]=json_data["導覽點設定 (guides)"]
        data = st.session_state['session_state']

        st.sidebar.json(json_data)

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def show_home():
    st.title("Welcome to Json-Creation webapp!")
    st.write("Please use the sidebar to navigate.")


def show_resources():
    st.title("資源設定")
    with st.form(key='resources_form'):
        key = st.text_input("Key")
        type_ = st.selectbox("Type", options=["video", "image"])
        url = st.text_input("URL")
        submit = st.form_submit_button("Add Resource")
        if submit:
            st.session_state['session_state']["resources"].append({"key": key, "type": type_, "url": url})

    if st.session_state['session_state']["resources"]:
        resources_to_delete = st.sidebar.selectbox("Select a resource to delete",
                                           options=range(len(st.session_state['session_state']["resources"])))
        if st.sidebar.button("Delete selected resource"):
            del st.session_state['session_state']["resources"][resources_to_delete]
    edited_df = st.data_editor(st.session_state['session_state']["resources"],num_rows="dynamic",hide_index=False,use_container_width = True)
    st.session_state['session_state']["resources"] = edited_df


def show_ads():
    st.title("廣告設定")
    # Prepare resources keys for selection
    resource_keys = [resource['key'] for resource in st.session_state['session_state']["resources"]]

    if 'current_ad' not in st.session_state:
        st.session_state['current_ad'] = {"語⾔": None, "廣告": []}

    ad_lag = st.selectbox("廣告語言", options=["zh-TW", "en-US", "ja-JP", "ko-KR", "en-AU"])
    st.session_state['current_ad']["語⾔"] = ad_lag

    # Determine the available orders based on the current ad
    available_orders = list(set(range(1, 7)) - set([item['順序'] for item in st.session_state['current_ad']["廣告"]]))

    # Create two columns for order and resource selection
    col1, col2 = st.columns(2)
    with col1:
        ad_order = st.selectbox("廣告順序", options=available_orders)
    with col2:
        ad_resource = st.selectbox("廣告資源", options=resource_keys)

    with st.form(key='ads_form'):
        col3, col4 = st.columns(2)
        with col3:
            add_element = st.form_submit_button("添加廣告元素")
            if add_element:
                st.session_state['current_ad']["廣告"].append({"順序": ad_order, "資源": ad_resource})
                st.write(st.session_state['current_ad']["廣告"])  # 顯示目前添加的廣告元素

        with col4:
            finish_ad = st.form_submit_button("結束目前添加")
            if finish_ad:
                st.session_state['session_state']["ads"].append(st.session_state['current_ad'])
                st.session_state['current_ad'] = {"語⾔": None, "廣告": []}

    # Show ads
    if st.session_state['session_state']["ads"]:
        ads_index_options = list(range(len(st.session_state['session_state']["ads"])))
        ad_to_delete_index = st.sidebar.selectbox("選擇要刪除的廣告", options=ads_index_options)
        if st.sidebar.button("刪除選擇的廣告"):
            del st.session_state['session_state']["ads"][ad_to_delete_index]

    # Edit data
    edited_df = st.data_editor(st.session_state['session_state']["ads"], num_rows="dynamic", hide_index=False,
                               use_container_width=True)
    st.session_state['session_state']["ads"] = edited_df


def show_talks():
    st.title("⽂本設定")
    with st.form(key='talks_form'):
        talk_title = st.text_input("⽂本標題")
        talk_content = st.text_area("⽂本內容")
        audio_url = st.text_input("聲音URL")
        submit = st.form_submit_button("Add Talk")
        if submit:
            st.session_state['session_state']["talks"].append({"title": talk_title, "content": talk_content, "audio_url": audio_url})


    if st.session_state['session_state']["talks"]:
        talks_to_delete = st.sidebar.selectbox("Select a talk to delete", options=range(len(st.session_state['session_state']["talks"])))
        if st.sidebar.button("Delete selected talk"):
            del st.session_state['session_state']["talks"][talks_to_delete]
    edited_df = st.data_editor(st.session_state['session_state']["talks"], num_rows="dynamic", hide_index=False, use_container_width = True)
    st.session_state['session_state']["talks"] = edited_df


def show_routes():
    st.title("路線設定")

    # Initialize route points list in session state if not already present
    if 'route_points' not in st.session_state:
        st.session_state['route_points'] = []

    route_name = st.text_input("路線名稱")
    route_description = st.text_area("路線描述")

    col1, col2 = st.columns(2)

    if col1.button('添加導覽點'):
        st.session_state['route_points'].append("")

    if col2.button('删除最後導覽點'):
        if st.session_state['route_points']:
            st.session_state['route_points'].pop()

    for idx, _ in enumerate(st.session_state['route_points']):
        st.session_state['route_points'][idx] = st.text_input(f"導覽點 {idx + 1}",
                                                              value=st.session_state['route_points'][idx])
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button('導覽路線添加'):
        if 'routes' not in st.session_state['session_state']:
            st.session_state['session_state']['routes'] = []
        st.session_state['session_state']['routes'].append(
            {"導覽路線": route_name, "路線描述": route_description, "導覽點s": st.session_state['route_points'][:]})
        st.session_state['route_points'].clear()

    if st.session_state['session_state']["routes"]:
        routes_to_delete = st.sidebar.selectbox("Select a route to delete",
                                                options=range(len(st.session_state['session_state']["routes"])))
        if st.sidebar.button("Delete selected route"):
            del st.session_state['session_state']["routes"][routes_to_delete]

    edited_df = st.data_editor(st.session_state['session_state']["routes"], num_rows="dynamic", hide_index=False,
                               use_container_width=True)
    st.session_state['session_state']["routes"] = edited_df


def show_localizations():
    st.title("本地化設定")
    # Initialize selected_routes list in session state if not already present
    if 'selected_routes' not in st.session_state:
        st.session_state['selected_routes'] = []

    lang_option = st.selectbox("語言", options=["zh-TW", "en-US", "ja-JP", "ko-KR", "en-AU"])
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.session_state['session_state']["routes"]:
        route_names = [route["導覽路線"] for route in st.session_state['session_state']["routes"]]

        if st.button("新增路線"):
            st.session_state['selected_routes'].append("")  # Add a new route selection

        # For each route selection, create a selectbox
        for i, _ in enumerate(st.session_state['selected_routes']):
            st.session_state['selected_routes'][i] = st.selectbox(f"選擇路線 {i+1}", options=route_names, key=f"route_selection_{i}")

    else:
        st.write("請先填寫路線設定欄位")
    st.markdown("<hr>", unsafe_allow_html=True)
    submit = st.button("導入本地化設定")
    if submit:
        if 'localizations' not in st.session_state['session_state']:
            st.session_state['session_state']['localizations'] = []
        st.session_state['session_state']['localizations'].append(
            {"語言": lang_option, "路線s": st.session_state['selected_routes'][:]})
        st.session_state['selected_routes'].clear()

    # Delete localizations
    if 'localizations' in st.session_state['session_state']:
        localization_to_delete = st.sidebar.selectbox("Select a localization to delete",
                                                      options=range(len(st.session_state['session_state']['localizations'])))
        if st.sidebar.button("Delete selected localization"):
            del st.session_state['session_state']['localizations'][localization_to_delete]

    # Edit data
    edited_df = st.data_editor(st.session_state['session_state']['localizations'], num_rows="dynamic", hide_index=False,
                               use_container_width=True)
    st.session_state['session_state']["localizations"] = edited_df



def show_parts():
    st.title("段落設定")

    # Initialize behaviors list in session state if not already present
    if 'behaviors' not in st.session_state:
        st.session_state['behaviors'] = []

    part_name = st.text_input("段落名稱")

    # Add behavior button
    if st.button('添加行為'):
        st.session_state['behaviors'].append({"行為類型": "", "接續方式": "", "Content": ""})

    # Remove last behavior button
    if st.button('删除最後行為'):
        if st.session_state['behaviors']:
            st.session_state['behaviors'].pop()

    # For each behavior, create a form
    for idx, _ in enumerate(st.session_state['behaviors']):
        with st.form(key=f'behavior_{idx}_form'):
            st.session_state['behaviors'][idx]['行為類型'] = st.selectbox("行為類型", ["image", "text"], key=f'behavior_{idx}_type')
            st.session_state['behaviors'][idx]['接續方式'] = st.selectbox("接續方式", ["follow", "continue"], key=f'behavior_{idx}_follow')
            st.session_state['behaviors'][idx]['Content'] = st.text_input("Content", key=f'behavior_{idx}_content')
            st.form_submit_button("確定行為")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Add part button
    if st.button('添加段落'):
        if 'parts' not in st.session_state['session_state']:
            st.session_state['session_state']['parts'] = []
        st.session_state['session_state']['parts'].append(
            {"段落": part_name, "行為s": st.session_state['behaviors'][:]})
        st.session_state['behaviors'].clear()

    # Delete parts
    if st.session_state['session_state']["parts"]:
        parts_to_delete = st.sidebar.selectbox("選擇要刪除的段落",
                                               options=range(len(st.session_state['session_state']["parts"])))
        if st.sidebar.button("刪除選擇的段落"):
            del st.session_state['session_state']["parts"][parts_to_delete]

    # Edit data
    edited_df = st.data_editor(st.session_state['session_state']["parts"], num_rows="dynamic", hide_index=False,
                               use_container_width=True)
    st.session_state['session_state']["parts"] = edited_df


def show_guides():
    st.title("導覽點設定")

    if st.session_state['session_state']["routes"]:
        guide_options = []
        for route in st.session_state['session_state']["routes"]:
            if '導覽點s' in route:
                guide_options.extend(route['導覽點s'])

        guide_name = st.selectbox("導覽點名稱", options=guide_options)

        # Collect path data
        path_list = st.session_state.get('path_list', [])
        path_entry = st.text_input('路徑')
        if st.button("添加路徑"):
            path_list.append(path_entry)
            st.session_state['path_list'] = path_list
        if st.button("刪除最後一個路徑"):
            if path_list:
                path_list.pop()
                st.session_state['path_list'] = path_list
        st.write("已添加的路徑: ", path_list)

        # Collect paragraph data
        paragraph_list = st.session_state.get('paragraph_list', [])
        paragraph_order = st.selectbox('順序', list(range(1, 7)))
        paragraph_type = st.selectbox('類型', ['移動途中', '已到導覽點上', '閒置中'])
        paragraph_content = st.selectbox("段落", options=[part['段落'] for part in
                                                        st.session_state['session_state']["parts"]])
        if st.button("添加段落"):
            paragraph_list.append({"順序": paragraph_order, "類型": paragraph_type, "段落": paragraph_content})
            st.session_state['paragraph_list'] = paragraph_list
        st.write("已添加的段落: ", paragraph_list)
        st.markdown("<hr>", unsafe_allow_html=True)

        if st.button("添加導覽點"):
            if 'guides' not in st.session_state['session_state']:
                st.session_state['session_state']['guides'] = []
            st.session_state['session_state']['guides'].append(
                {"導覽點": guide_name, "路徑": path_list, "段落s": paragraph_list})
            path_list = []
            paragraph_list = []
            st.session_state['path_list'] = path_list
            st.session_state['paragraph_list'] = paragraph_list
    else:
        st.write("請先添加路線並設定導覽點。")

    # Delete guides
    if st.session_state['session_state']["guides"]:
        guides_to_delete = st.sidebar.selectbox("選擇要刪除的導覽點",
                                                options=range(len(st.session_state['session_state']["guides"])))
        if st.sidebar.button("刪除選擇的導覽點"):
            del st.session_state['session_state']["guides"][guides_to_delete]

    # Edit data
    edited_df = st.data_editor(st.session_state['session_state']["guides"], num_rows="dynamic", hide_index=False,
                               use_container_width=True)
    st.session_state['session_state']["guides"] = edited_df


# st.markdown("<hr>", unsafe_allow_html=True)
def generate_json():
    data = {
        "資源設定 (resources)": st.session_state['session_state']["resources"],
        "廣告設定 (ads)": st.session_state['session_state']["ads"],
        "⽂本設定 (talks)": st.session_state['session_state']["talks"],
        "路線設定 (routes)": st.session_state['session_state']["routes"],
        "本地化設定 (localizations)": st.session_state['session_state']["localizations"],
        "段落設定 (parts)": st.session_state['session_state']["parts"],
        "導覽點設定 (guides)": st.session_state['session_state']["guides"]
    }
    st.json(data)
    json_data = json.dumps(data, ensure_ascii=False)
    show_Json_graph(json_data)
    st.download_button("Download JSON file", data=json.dumps(data, ensure_ascii=False).encode("utf-8"), file_name="data.json", mime="application/json")

if __name__ == "__main__":
    main()
