import subprocess
import time
import sys

participants = [
    ("조은정", "010-7137-2294"),
    ("박세진", "010-3385-9343"),
    ("이하연", "010-6521-1272"),
    ("강수민", "010-3226-2056"),
    ("나예진", "010-7338-1048"),
    ("방세희", "010-5169-1569"),
    ("김하은", "010-8280-9943"),
    ("정채윤", "010-5427-4709"),
    ("정지연", "010-5356-9518"),
    ("고윤서", "010-3597-5752"),
    ("최명주", "010-5953-0668")
]

template = """[연세대학교 Vibe Design 101 워크숍 후기 대시보드 오픈]

안녕하세요, {name}님.
연세대학교 Vibe Design 101 특강 워크숍에 함께해 주셔서 감사합니다.

참석자 여러분께서 정성껏 작성해 주신 만족도 조사 결과와 생생한 워크숍 후기를 한눈에 보실 수 있는 대시보드 페이지가 개설되었습니다. 
아래 링크에서 우리 워크숍의 멋진 기록과 피드백 결과물들을 확인해 보세요!

▶ 워크숍 후기 대시보드 확인: https://vibedesign.cowcowwow.kr

함께해 주신 소중한 시간에 다시 한번 감사드리며, 다음에 더 유익한 기회로 뵙겠습니다. 

소재환 드림"""

def send_via_applescript(phone, message):
    # macOS Messages 앱을 이용한 문자 전송 AppleScript
    # iMessage 혹은 SMS가 연동되어 있어야 하며, 권한이 허용되어야 합니다.
    applescript_code = f'''
    tell application "Messages"
        set targetBuddy to buddy "{phone}" of service 1
        send "{message}" to targetBuddy
    end tell
    '''
    process = subprocess.Popen(['osascript', '-e', applescript_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return process.returncode, out, err

if __name__ == "__main__":
    print("==================================================")
    print("연세대학교 Vibe Design 101 워크숍 후기 안내 메시지 발송기")
    print("==================================================")
    print(f"총 {len(participants)}명의 참가자에게 발송을 준비합니다.")
    
    # 사용자 확인 단계 (CLI 수동 실행 대비)
    if len(sys.argv) < 2 or sys.argv[1] != "--yes":
        confirm = input("발송을 진행하시겠습니까? (y/n): ")
        if confirm.lower() != 'y':
            print("발송을 취소했습니다.")
            sys.exit(0)

    for idx, (name, phone) in enumerate(participants, 1):
        msg = template.replace("{name}", name)
        print(f"[{idx}/{len(participants)}] {name}({phone}) 발송 중...")
        
        # 줄바꿈 이스케이프 처리하여 AppleScript로 전달
        escaped_msg = msg.replace('"', '\\"').replace('\n', '\\n')
        code, out, err = send_via_applescript(phone, escaped_msg)
        
        if code != 0:
            print(f"  ❌ 발송 실패: {err.decode('utf-8').strip()}")
            print("     (macOS 시스템 환경설정 -> 개인정보 및 보안 -> '자동화'에서 권한 설정을 확인하세요)")
        else:
            print(f"  ✅ 발송 성공")
            
        time.sleep(2)  # 발송 간격 딜레이 (안전 장치)
        
    print("모든 발송 프로세스가 종료되었습니다.")
