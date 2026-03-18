import winreg
import sys

def set_windows_update_pause_days():
    """
    设置 Windows Update 暂停更新的最大天数（FlightSettingsMaxPauseDays）
    对应 BAT 命令：reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\WindowsUpdate\\UX\\Settings" /v FlightSettingsMaxPauseDays /t reg_dword /d 10240 /f
    """
    # 定义注册表路径和参数（这里用原始字符串 r"" 避免转义）
    reg_path = r"SOFTWARE\Microsoft\WindowsUpdate\UX\Settings"
    reg_key_name = "FlightSettingsMaxPauseDays"
    reg_value = 10240  # DWORD 类型的值
    reg_hive = winreg.HKEY_LOCAL_MACHINE  # 对应 HKLM

    try:
        # 打开/创建注册表项（KEY_WRITE 表示写入权限）
        # 注意：操作 HKLM 需要管理员权限！
        key = winreg.OpenKey(reg_hive, reg_path, 0, winreg.KEY_WRITE)
    except FileNotFoundError:
        # 如果路径不存在，创建该注册表项
        key = winreg.CreateKey(reg_hive, reg_path)
    except PermissionError:
        print("错误：需要以管理员身份运行此脚本！")
        sys.exit(1)
    except Exception as e:
        print(f"打开/创建注册表项失败：{e}")
        sys.exit(1)

    try:
        # 设置 DWORD 类型的注册表值（/t reg_dword 对应 winreg.REG_DWORD）
        # /f 强制覆盖已存在的值，winreg.SetValueEx 本身就会覆盖
        winreg.SetValueEx(key, reg_key_name, 0, winreg.REG_DWORD, reg_value)
        print(f"成功设置 {reg_key_name} = {reg_value}")
    except Exception as e:
        print(f"设置注册表值失败：{e}")
    finally:
        # 关闭注册表项
        winreg.CloseKey(key)

if __name__ == "__main__":
    set_windows_update_pause_days()