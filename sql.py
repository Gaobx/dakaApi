# -*- coding: utf-8 -*-

import config
import pymysql
import time
import traceback


# import ai_judge


class sql(object):
    def __init__(self):
        self.db = pymysql.connect(config.mql_url,
                                  config.mql_user,
                                  config.mql_pswd,
                                  config.mql_db,
                                  charset="utf8")

    def login(self, params):
        """
        :param params: user_id，作为主键; user_name
        :return: 
            若是新用户，return {'code': '1001', 'msg':'creat new user successfully'}
            若已存在用户，return {'code':'1002', 'msg':'login in successfully'}
        """
        sql_login = "select user_id \
                    from user_info \
                    where user_id = '%s'" % (params['user_id'])

        sql_create = "insert into user_info(user_id, user_name, user_image) \
        values ('%s', '%s', '%s')" % (
            params['user_id'], params['user_name'], params['user_image'])

        try:
            cursor = self.db.cursor()
            cursor.execute(sql_login)
            result = cursor.fetchall()
            if len(result) != 0:
                sql_update = "update user_info set \
                user_name = '%s', user_image = '%s' \
                where user_id = '%s'" % \
                             (params['user_name'], params['user_image'], params['user_id'])
                cursor.execute(sql_update)
                cursor.close()
                self.db.commit()

                return {'code': '1002', 'msg': 'login in successfully'}

            result = cursor.execute(sql_create)
            # print(result)
            cursor.close()

            self.db.commit()
            return {'code': '1001', 'msg': 'creat new user successfully'}

        except BaseException as e:
            print(e)
            self.db.rollback()
            return {'code': '1003', 'msg': ' login error'}

    def get_user_info(self, params):

        sql_get_user_info = \
            "select user_id, user_name, sexual, \
                district, born, user_intro, user_image \
            from user_info \
            where user_id = '%s'" % (params['user_id'])

        try:
            cursor = self.db.cursor()
            cursor.execute(sql_get_user_info)
            record = cursor.fetchone()
            result = {}
            result['user_id'] = record[0]
            result['user_name'] = record[1]
            result['sexual'] = record[2]
            result['district'] = record[3]
            result['born'] = record[4]
            result['user_intro'] = record[5]
            result['user_image'] = record[6]

            cursor.close()
            return result
        except BaseException as e:
            print(e)
            return {'code': '1031', 'msg': 'get user info failed'}



    def get_slide_images(self):
        """
        返回滑动图片url
        :return: 
        """
        sql = "select option_value \
                from config \
                where option_name REGEXP '%s'" % ('slide_image_')

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except BaseException as e:
            print(e)
            return False

    def create_group(self, params):
        """
        :param params: some info
        :return: 
        """

        time_now = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(time.time()))
        if 'group_image' in params:
            sql_gp_info = "insert into group_info( \
                        group_id, group_name, group_image, create_date, \
                        group_intro, money, member_num, \
                        limit_num, duration, is_finished, type) \
                        values \
                        (default, '%s', '%s', '%s', '%s', %d, 1, %d, %d, 'no', '%s')" % \
                          (params['group_name'], params['group_image'],
                           str(time_now), params['group_intro'],
                           params['money'], params['limit_num'],
                           params['duration'], params['type'])
        else:

            sql_gp_info = "insert into group_info( \
                        group_id, group_name, create_date, group_intro, \
                        money, member_num, limit_num, duration, \
                        is_finished, type) \
                        values \
                        (default, '%s', '%s', '%s', %d, 1, %d, %d, 'no', '%s')" % \
                          (params['group_name'], str(time_now),
                           params['group_intro'],
                           int(params['money']), int(params['limit_num']),
                           int(params['duration']), params['type'])

        try:
            cursor = self.db.cursor()
            cursor.execute(sql_gp_info)
            tmp = "select last_insert_id() "
            cursor.execute(tmp)
            gp_id = cursor.fetchone()[0]
            sql_gp_usr = "insert into group_user( \
                group_id, user_id, is_creater, join_date) \
                values(%d, '%s', '%s', '%s')" % (
                gp_id, params['user_id'], 'yes', str(time_now))
            cursor.execute(sql_gp_usr)
            cursor.close()
            self.db.commit()

            return {'code': '1007', 'msg': 'create group successfully', 'group_id': gp_id}
        except BaseException as e:
            print(e)
            self.db.rollback()
            return {'code': '1006', 'msg': 'create group failed'}

    def get_my_groups(self, params):
        if 'is_finished' in params:
            is_fnsd = params['is_finished']
        else:
            is_fnsd = 'no'

        if is_fnsd == 'full':
            sql_get_groups = \
                "select group_id, user_id, is_creater, group_name, \
                    group_image, create_date, group_intro, money, \
                    member_num, limit_num, duration, is_finished, type \
                from group_user natural join group_info \
                where user_id = '%s' \
                order by create_date desc" % (params['user_id'])
        else:
            sql_get_groups = \
                "select group_id, user_id, is_creater, group_name, \
                    group_image, create_date, group_intro, money, \
                    member_num, limit_num, duration, is_finished, type \
                from group_user natural join group_info \
                where user_id = '%s' and is_finished = '%s' \
                order by create_date desc" % (
                    params['user_id'], is_fnsd)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql_get_groups)
            # results = self.cursor.fetchall()
            results = []
            for i in range(cursor.rowcount):
                record = cursor.fetchone()
                result = {}

                result['group_id'] = record[0]
                result['user_id'] = record[1]
                result['is_creater'] = record[2]
                result['group_name'] = record[3]
                result['group_image'] = record[4]
                result['create_date'] = record[12]
                result['group_intro'] = record[5]
                result['money'] = record[6]
                result['member_num'] = record[7]
                result['limit_num'] = record[8]
                result['duration'] = record[9]
                result['is_finished'] = record[10]
                result['type'] = record[11]
                result['daka_records'] = []

                sql_my_daka_records = "select date from daka_record \
                where group_id = '%d' and user_id ='%s'" % (
                    result['group_id'], result['user_id'])
                cursor2 = self.db.cursor()
                cursor2.execute(sql_my_daka_records)
                for j in range(cursor2.rowcount):
                    daka_record = cursor2.fetchone()
                    result['daka_records'].append(daka_record[0])
                cursor2.close()

                results.append(result)

            cursor.close()
            return results
        except BaseException as e:
            print(e)
            return {'code': '1009', 'msg': 'get groups error'}

    def get_recommend_groups(self, params):

        if 'type' not in params:
            sql_get_re_grps = \
                "select group_id, group_name, group_image, \
                group_intro, money, member_num, limit_num, \
                duration, is_finished, type, create_date, \
                user_id, is_creater \
                from group_info natural join group_user\
                where user_id != '%s' \
                    and is_finished = 'no' \
                    and member_num < limit_num \
                    and is_creater = 'yes' \
                order by member_num desc" % (
                    params['user_id']
                )
        else:
            sql_get_re_grps = \
                "select group_id, group_name, group_image, \
                group_intro, money, member_num, limit_num, \
                duration, is_finished, type, create_date, \
                user_id, is_creater \
                from group_info natural join group_user\
                where user_id != '%s' \
                    and is_finished = 'no' \
                    and member_num < limit_num \
                        and is_creater = 'yes' \
                        and type == '%s' \
                order by member_num desc" % (
                    params['user_id'], params['type']
                )

        try:
            cursor = self.db.cursor()
            cursor.execute(sql_get_re_grps)
            results = []
            for i in range(cursor.rowcount):
                record = cursor.fetchone()
                result = {}
                result['group_id'] = record[0]
                result['group_name'] = record[1]
                result['group_image'] = record[2]
                result['group_intro'] = record[3]
                result['money'] = record[4]
                result['member_num'] = record[5]
                result['limit_num'] = record[6]
                result['duration'] = record[7]
                result['is_finished'] = record[8]
                result['type'] = record[9]
                result['create_date'] = record[10]
                result['user_id'] = record[11]
                result['is_creater'] = record[12]
                result['user_list'] = []

                cursor2 = self.db.cursor()
                sql_get_grp_usr_list = \
                    "select user_id from group_user \
                    where is_creater = 'yes' and group_id = %d \
                    UNION \
                    select user_id from group_user \
                    where is_creater = 'no' and group_id = %d " % (
                        int(result['group_id']), int(result['group_id']) )
                cursor2.execute(sql_get_grp_usr_list)

                for j in range(cursor2.rowcount):
                    daka_record = cursor2.fetchone()
                    result['user_list'].append(daka_record[0])
                cursor2.close()

                results.append(result)

            cursor.close()
            return results

        except BaseException as e:
            print(e)
            return {'code': '1025', 'msg': 'get recommend groups error'}

    def join_group(self, params):

        time_now = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(time.time()))

        sql_check_num = "select member_num, limit_num \
            from group_info \
            where group_id = %d" % (int(params['group_id']))
        sql_insert_to_group_user = \
            "insert into group_user(group_id, user_id, is_creater, join_date) \
            values ( %d, '%s', 'no', '%s' )" % (
                int(params['group_id']), params['user_id'], str(time_now) )
        sql_update_grp_info = \
            "update group_info set member_num = member_num+'1' \
            where group_id = %d " % (int(params['group_id']))

        try:
            cursor = self.db.cursor()
            cursor.execute(sql_check_num)
            number = cursor.fetchone()
            mem_num = number[0]
            lim_num = number[1]
            if mem_num >= lim_num:
                cursor.close()
                return {'code': '1028', 'msg': 'he number reached the upper limit'}

            cursor.execute(sql_insert_to_group_user)
            cursor.execute(sql_update_grp_info)
            cursor.close()

            self.db.commit()
            return {'code': '1026', 'msg': 'join group successfully'}

        except BaseException as e:
            print(e)
            self.db.rollback()
            return {'code': '1029', 'msg': 'join group failed'}

    def commit_daka(self, params):
        if 'daka_images' in params:
            daka_images = params['daka_images']
        else:
            daka_images = [
                "http://file.24en.com/d/file/exam/cet/2015-12-16/9cbc700b28e080290a2cf935ffce2036.jpg"]
        if 'daka_words' in params:
            daka_words = params['daka_words']
        else:
            daka_words = "今日打卡"
        now_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(time.time()))

        sql_get_group_type = "select type from group_info where group_id = '%s'" % (
            int(params['group_id']))

        try:
            csr = self.db.cursor()
            csr.execute(sql_get_group_type)
            type = csr.fetchone()
            csr.close()
            # 图像识别判断打卡
            # judge_result = ai_judge.judge(type, daka_images)
            judge_result = "未评定"

            sql_commit_daka = "insert into daka_record( \
                    group_id, user_id, date, words, machine_judge) values \
                    (%d, '%s', '%s', '%s', '%s')" % (
                int(params['group_id']), params['user_id'],
                str(now_time), daka_words, judge_result)

            cursor = self.db.cursor()
            cursor.execute(sql_commit_daka)
            cursor.close()
            for i in daka_images:
                sql_commit_daka_images = "insert into daka_images(\
                group_id, user_id, date, image_url) values \
                (%d, '%s', '%s', '%s')" % (
                    int(params['group_id']), params['user_id'], str(now_time), i)
                cursor2 = self.db.cursor()
                cursor2.execute(sql_commit_daka_images)
                cursor2.close()

            self.db.commit()
            return {'code': '1010', 'msg': 'daka commit success'}
        except BaseException as e:
            print(e)
            self.db.rollback()
            return {'code': '1012', 'msg': 'daka commit error'}

    def commit_appeal(self, params):
        if 'content' in params:
            content = params['content']
        else:
            content = "NULL"
        sql_commit_appeal = "insert into appeal(\
        group_id, user_id, date, content) values (\
        %d, '%s', '%s', '%s')" % (
            int(params['group_id']), params['user_id'], params['date'], content)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql_commit_appeal)
            cursor.close()
            self.db.commit()
            return {'code': '1013', 'msg': 'appeal commit success'}

        except BaseException as e:
            print(e)
            self.db.rollback()
            return {'code': '1015', 'msg': 'appeal commit error'}

    def get_my_appeal(self, params):

        sql_get_my_appeal = "select * from appeal natural join \
        group_info where user_id = '%s'" % (params['user_id'])

        try:
            cursor = self.db.cursor()
            cursor.execute(sql_get_my_appeal)

            results = []
            for i in range(cursor.rowcount):
                record = cursor.fetchone()
                result = {}
                result['group_id'] = record[0]
                result['user_id'] = record[1]
                result['date'] = record[2]
                result['content'] = record[3]
                result['result'] = record[4]
                result['group_name'] = record[5]

                results.append(result)

            cursor.close()
            return results
        except BaseException as e:
            print(e)
            return {'code': '1017', 'msg': 'get my appeal error'}

    def commit_judgement(self, params):

        sql_cmmt_jdg = "insert into judge_record( \
        group_id, user_id, date, assessor_id, is_passed, ass_time) \
        values (%d, '%s', '%s', '%s', '%s', now())" % (
            int(params['group_id']), params['user_id'], params['date'],
            params['assessor_id'], params['is_passed'])

        sql_alter_jg_rcd = "update daka_record set judge_count = judge_count+'1'\
        where group_id = %d and user_id = '%s' and date = '%s'" % (
            int(params['group_id']), params['user_id'], params['date'])

        sql_alter_jg_yes_rcd = "update daka_record set judge_yes_cnt = judge_yes_cnt+'1'\
               where group_id = %d and user_id = '%s' and date = '%s'" % (
            int(params['group_id']), params['user_id'], params['date'])

        try:
            cursor = self.db.cursor()
            cursor.execute(sql_cmmt_jdg)
            cursor.execute(sql_alter_jg_rcd)
            if params['is_passed'] == 'yes' or params['ispassed'] == '通过':
                cursor.execute(sql_alter_jg_yes_rcd)
            cursor.close()
            self.db.commit()
            return {'code': '1018', 'msg': 'commit judgement successfully'}
        except BaseException as e:
            print(e)
            self.db.rollback()
            return {'code': '1020', 'msg': 'commit judgement error'}

    def get_others_daka_info(self, params):

        try:
            cursor = self.db.cursor()
            sql_judge_num = "select option_value from config \
            where option_name = '%s'" % 'judge_num'
            cursor.execute(sql_judge_num)
            judge_num = int(cursor.fetchone()[0])
            print (judge_num)

            sql_g_o_dk_i = \
                "select group_id, user_id, date, words, machine_judge, \
                judge_result, judge_count, judge_yes_cnt, group_name, \
                group_image, group_intro, money, member_num, limit_num, \
                duration, is_finished, type, create_date \
            from (daka_record natural join group_info)  \
            where user_id != '%s' and judge_count <= %d \
                and not exists ( select * from judge_record as j  \
                                where daka_record.group_id = j.group_id and \
                                    daka_record.user_id = j.user_id and \
                                    daka_record.date = j.date and \
                                    j.assessor_id = '%s' ) \
            order by date, judge_count asc" % (
                    params['user_id'], judge_num, params['user_id'])

            cursor.execute(sql_g_o_dk_i)
            # result = cursor.fetchone()
            while True:
                record = cursor.fetchone()
                if record is None:
                    result = {'code': '1021', 'msg': 'no user need to judge'}
                    break

                result = {}
                result['group_id'] = record[0]
                result['user_id'] = record[1]
                result['daka_date'] = record[2]
                result['words'] = record[3]
                result['machine_judge'] = record[4]
                result['judge_result'] = record[5]
                result['judge_count'] = record[6]
                result['judge_yes_cnt'] = record[7]
                result['group_name'] = record[8]
                result['group_image'] = record[9]
                result['group_intro'] = record[10]
                result['money'] = record[11]
                result['member_num'] = record[12]
                result['limit_num'] = record[13]
                result['duration'] = record[14]
                result['is_finished'] = record[15]
                result['type'] = record[16]
                result['group_create_date'] = record[17]

                if 'type' not in params:
                    break
                if params['type'] == result['type']:
                    break
            cursor.close()

            return result

        except BaseException as e:
            print(e)
            return {'code': '1022', 'msg': 'get others daka info error'}

